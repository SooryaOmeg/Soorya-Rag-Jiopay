import json
import time
import requests
import numpy as np
import os
import psutil
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai


class RAGEvaluator:
    def __init__(self, api_url, gemini_key=None, model_name="multi-qa-mpnet-base-dot-v1"):
        self.api_url = api_url
        self.embedder = SentenceTransformer(model_name)

        # Optional LLM-as-judge
        if gemini_key:
            genai.configure(api_key=gemini_key)
            self.llm_judge = genai.GenerativeModel("gemini-2.5-flash")
        else:
            self.llm_judge = None

    # ----------------- Utility Functions -----------------
    def get_grade(self, score):
        """Convert similarity score to letter grade."""
        if score >= 0.7: return "A"
        elif score >= 0.5: return "B" 
        elif score >= 0.3: return "C"
        elif score >= 0.2: return "D"
        else: return "F"

    # ----------------- Retrieval -----------------
    def query_system(self, query):
        """Query the RAG system and measure latency."""
        start_time = time.time()
        try:
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={"message": query},
                timeout=100
            )
            latency = (time.time() - start_time) * 1000  # ms
            return response.json(), latency
        except Exception as e:
            print(f"Query error: {e}")
            return None, 0

    def calculate_retrieval_metrics(self, generated_answer, expected_answer):
        """Improved retrieval metrics with continuous scoring and better thresholds."""
        if not generated_answer or not expected_answer:
            return {"similarity_score": 0, "quality_grade": "F", "meets_threshold": False}

        sim = util.cos_sim(
            self.embedder.encode(expected_answer, convert_to_tensor=True),
            self.embedder.encode(generated_answer, convert_to_tensor=True)
        ).item()

        # Use more reasonable threshold (0.3 instead of 0.6)
        meets_threshold = sim > 0.3
        grade = self.get_grade(sim)

        return {
            "similarity_score": sim,
            "quality_grade": grade,
            "meets_threshold": meets_threshold,
            # Keep old metrics for compatibility but make them continuous
            "p_at_1": sim if meets_threshold else 0,
            "recall_at_k": sim,
            "mrr": sim
        }

    # ----------------- Answer Quality -----------------
    def evaluate_answer(self, query, generated_answer, citations, expected_answer):
        """Improved answer evaluation with better metrics and continuous scoring."""
        results = {}

        # Skip evaluation if answers are missing
        if not generated_answer or not expected_answer:
            return {
                "exact_match": 0,
                "semantic_similarity": 0,
                "faithfulness": 0,
                "completeness": 0,
                "relevance": 0,
                "overall_quality": 0,
                "human_notes": "Missing answer data"
            }

        # Encode once for efficiency
        expected_emb = self.embedder.encode(expected_answer, convert_to_tensor=True)
        gen_emb = self.embedder.encode(generated_answer, convert_to_tensor=True)
        query_emb = self.embedder.encode(query, convert_to_tensor=True)

        # 1. Improved exact match (using normalized token overlap)
        expected_tokens = set(expected_answer.lower().split())
        gen_tokens = set(generated_answer.lower().split())
        if expected_tokens:
            results["exact_match"] = len(expected_tokens & gen_tokens) / len(expected_tokens)
        else:
            results["exact_match"] = 0

        # 2. Semantic similarity (main metric)
        results["semantic_similarity"] = util.cos_sim(expected_emb, gen_emb).item()

        # 3. Relevance to original query
        results["relevance"] = util.cos_sim(query_emb, gen_emb).item()

        # 4. Improved faithfulness check
        if citations and any(c.get("chunk", "") for c in citations):
            # Use actual citations
            citation_texts = [c.get("chunk", "")[:300] for c in citations if c.get("chunk", "")]
            if citation_texts:
                citation_text = " ".join(citation_texts)
                citation_emb = self.embedder.encode(citation_text, convert_to_tensor=True)
                results["faithfulness"] = util.cos_sim(gen_emb, citation_emb).item()
            else:
                results["faithfulness"] = results["semantic_similarity"] * 0.8  # Penalty for no citations
        elif self.llm_judge:
            # Use LLM judge if available
            try:
                context = "\n".join([c.get("chunk", "")[:150] for c in citations])
                prompt = f"""Question: {query}
Generated Answer: {generated_answer}
Context/Citations: {context}

Rate how well the generated answer is supported by the context on a scale of 1-10.
Consider: Does the answer contradict the context? Is it fully supported? Is it partially supported?
Respond with only a number between 1-10."""
                
                resp = self.llm_judge.generate_content(prompt).text.strip()
                # Extract number from response
                score = float([word for word in resp.split() if word.replace('.', '').isdigit()][0])
                results["faithfulness"] = min(score / 10, 1.0)
            except Exception as e:
                print(f"LLM judge error: {e}")
                results["faithfulness"] = results["semantic_similarity"] * 0.9
        else:
            # Fallback: use semantic similarity with slight penalty
            results["faithfulness"] = results["semantic_similarity"] * 0.9

        # 5. Improved completeness (considers both similarity and relative length)
        length_ratio = len(generated_answer) / max(len(expected_answer), 1)
        # Penalize answers that are too short or too long
        length_factor = 1.0 if 0.5 <= length_ratio <= 2.0 else 0.8
        results["completeness"] = min(1.0, results["semantic_similarity"] * length_factor)

        # 6. Overall quality score (weighted combination)
        results["overall_quality"] = (
            0.35 * results["semantic_similarity"] +
            0.25 * results["completeness"] + 
            0.25 * results["faithfulness"] +
            0.15 * results["relevance"]
        )

        # 7. Human evaluation placeholder
        grade = self.get_grade(results["overall_quality"])
        results["human_notes"] = f"Auto-grade: {grade} (similarity: {results['semantic_similarity']:.3f})"

        return results

    # ----------------- Performance -----------------
    def system_usage(self):
        """Measure current system resource usage."""
        try:
            process = psutil.Process(os.getpid())
            mem_mb = process.memory_info().rss / (1024 * 1024)
            cpu_percent = psutil.cpu_percent(interval=0.1)
            return {"memory_mb": mem_mb, "cpu_percent": cpu_percent}
        except:
            return {"memory_mb": 0, "cpu_percent": 0}

    # ----------------- Full Evaluation Run -----------------
    def run_evaluation(self, queries_file):
        """Run complete evaluation on all queries in the file."""
        with open(queries_file, "r", encoding="utf-8") as f:
            queries = json.load(f)

        retrieval_scores, answer_scores, latencies = [], [], []
        results = []

        print(f"Starting evaluation of {len(queries)} queries...")
        
        for i, q in enumerate(queries):
            query = q.get("question", "")
            expected_answer = q.get("answer", "")

            print(f"[{i+1}/{len(queries)}] {query[:60]}...")

            # Query the system
            resp, latency = self.query_system(query)
            if not resp:
                print(f"  ❌ Failed to get response")
                continue

            generated = resp.get("response", "")
            citations = resp.get("citations", [])

            # Calculate metrics
            ret_metrics = self.calculate_retrieval_metrics(generated, expected_answer)
            ans_metrics = self.evaluate_answer(query, generated, citations, expected_answer)

            retrieval_scores.append(ret_metrics)
            answer_scores.append(ans_metrics)
            latencies.append(latency)

            # Show progress
            grade = self.get_grade(ans_metrics["overall_quality"])
            print(f"  ✅ Grade: {grade} (Quality: {ans_metrics['overall_quality']:.3f}, Latency: {latency:.0f}ms)")

            results.append({
                "query": query,
                "expected_answer": expected_answer,
                "generated_answer": generated,
                "retrieval_metrics": ret_metrics,
                "answer_metrics": ans_metrics,
                "latency_ms": latency,
                "citations_count": len(citations)
            })

        # Calculate final aggregated results
        if not results:
            print("❌ No successful queries to evaluate!")
            return None

        final_results = {
            "total_queries": len(results),
            "successful_queries": len([r for r in results if r["generated_answer"]]),
            
            "retrieval_metrics": {
                "avg_similarity_score": np.mean([r["similarity_score"] for r in retrieval_scores]),
                "avg_p_at_1": np.mean([r["p_at_1"] for r in retrieval_scores]),
                "avg_recall_at_k": np.mean([r["recall_at_k"] for r in retrieval_scores]),
                "avg_mrr": np.mean([r["mrr"] for r in retrieval_scores]),
                "threshold_pass_rate": np.mean([r["meets_threshold"] for r in retrieval_scores]),
            },
            
            "answer_quality": {
                "avg_exact_match": np.mean([a["exact_match"] for a in answer_scores]),
                "avg_semantic_similarity": np.mean([a["semantic_similarity"] for a in answer_scores]),
                "avg_faithfulness": np.mean([a["faithfulness"] for a in answer_scores]),
                "avg_completeness": np.mean([a["completeness"] for a in answer_scores]),
                "avg_relevance": np.mean([a["relevance"] for a in answer_scores]),
                "avg_overall_quality": np.mean([a["overall_quality"] for a in answer_scores]),
            },
            
            "performance": {
                "latency_mean": np.mean(latencies),
                "latency_p50": np.percentile(latencies, 50),
                "latency_p95": np.percentile(latencies, 95),
                "latency_max": np.max(latencies),
                **self.system_usage(),
                "cost_per_query": 0.0  # Update with actual costs if available
            },
            
            "grade_distribution": self._calculate_grade_distribution(answer_scores),
            "detailed_results": results
        }

        return final_results


    def run_evaluation_with_3rpm_limit(self, queries_file, max_queries=20):
        """Special evaluation for 3 RPM VoyageAI limit."""
        with open(queries_file, "r", encoding="utf-8") as f:
            queries = json.load(f)
        
        # Limit queries to avoid hitting rate limits
        queries = queries[:max_queries]
        
        retrieval_scores, answer_scores, latencies = [], [], []
        results = []
        
        print(f"🐌 Starting 3 RPM LIMITED evaluation of {len(queries)} queries...")
        print(f"   Delay: 25 seconds between queries")
        print(f"   Estimated time: {(len(queries) * 25) / 60:.1f} minutes")
        print("=" * 60)
        
        for i, q in enumerate(queries):
            query = q.get("question", "")
            expected_answer = q.get("answer", "")

            print(f"[{i+1}/{len(queries)}] {query[:50]}...")

            # Query the system
            resp, latency = self.query_system(query)
            
            if not resp:
                print(f"  ❌ API Error (likely rate limit)")
                # Add failed result
                results.append({
                    "query": query,
                    "expected_answer": expected_answer,
                    "generated_answer": "",
                    "retrieval_metrics": {
                        "similarity_score": 0, "quality_grade": "F", 
                        "meets_threshold": False, "p_at_1": 0, "recall_at_k": 0, "mrr": 0
                    },
                    "answer_metrics": {
                        "exact_match": 0, "semantic_similarity": 0, "faithfulness": 0,
                        "completeness": 0, "relevance": 0, "overall_quality": 0,
                        "human_notes": "Rate Limited"
                    },
                    "latency_ms": 0,
                    "citations_count": 0
                })
            else:
                generated = resp.get("response", "")
                citations = resp.get("citations", [])

                if not generated:
                    print(f"  ⚠️  Empty response")
                    grade = "F"
                    overall_quality = 0
                    ret_metrics = {
                        "similarity_score": 0, "quality_grade": "F",
                        "meets_threshold": False, "p_at_1": 0, "recall_at_k": 0, "mrr": 0
                    }
                    ans_metrics = {
                        "exact_match": 0, "semantic_similarity": 0, "faithfulness": 0,
                        "completeness": 0, "relevance": 0, "overall_quality": 0,
                        "human_notes": "Empty response"
                    }
                else:
                    # Calculate metrics normally
                    ret_metrics = self.calculate_retrieval_metrics(generated, expected_answer)
                    ans_metrics = self.evaluate_answer(query, generated, citations, expected_answer)
                    
                    retrieval_scores.append(ret_metrics)
                    answer_scores.append(ans_metrics)
                    
                    grade = self.get_grade(ans_metrics["overall_quality"])
                    overall_quality = ans_metrics["overall_quality"]

                results.append({
                    "query": query,
                    "expected_answer": expected_answer,
                    "generated_answer": generated,
                    "retrieval_metrics": ret_metrics,
                    "answer_metrics": ans_metrics,
                    "latency_ms": latency,
                    "citations_count": len(citations)
                })

                latencies.append(latency)
                print(f"  ✅ Grade: {grade} (Quality: {overall_quality:.3f}, Latency: {latency:.0f}ms)")

            # Critical: Wait 25 seconds between queries for 3 RPM limit
            if i < len(queries) - 1:
                print(f"  ⏳ Waiting 25s for VoyageAI rate limit...")
                time.sleep(25)

        # Calculate results only from successful queries
        successful_retrievals = [r for r in retrieval_scores if r["similarity_score"] > 0]
        successful_answers = [a for a in answer_scores if a["overall_quality"] > 0]
        
        final_results = {
            "total_queries": len(results),
            "successful_queries": len(successful_answers),
            "rate_limited_queries": len(results) - len(successful_answers),
            
            "retrieval_metrics": {
                "avg_similarity_score": np.mean([r["similarity_score"] for r in successful_retrievals]) if successful_retrievals else 0,
                "avg_p_at_1": np.mean([r["p_at_1"] for r in successful_retrievals]) if successful_retrievals else 0,
                "avg_recall_at_k": np.mean([r["recall_at_k"] for r in successful_retrievals]) if successful_retrievals else 0,
                "avg_mrr": np.mean([r["mrr"] for r in successful_retrievals]) if successful_retrievals else 0,
                "threshold_pass_rate": np.mean([r["meets_threshold"] for r in successful_retrievals]) if successful_retrievals else 0,
            },
            
            "answer_quality": {
                "avg_exact_match": np.mean([a["exact_match"] for a in successful_answers]) if successful_answers else 0,
                "avg_semantic_similarity": np.mean([a["semantic_similarity"] for a in successful_answers]) if successful_answers else 0,
                "avg_faithfulness": np.mean([a["faithfulness"] for a in successful_answers]) if successful_answers else 0,
                "avg_completeness": np.mean([a["completeness"] for a in successful_answers]) if successful_answers else 0,
                "avg_relevance": np.mean([a["relevance"] for a in successful_answers]) if successful_answers else 0,
                "avg_overall_quality": np.mean([a["overall_quality"] for a in successful_answers]) if successful_answers else 0,
            },
            
            "performance": {
                "latency_mean": np.mean(latencies) if latencies else 0,
                "latency_p50": np.percentile(latencies, 50) if latencies else 0,
                "latency_p95": np.percentile(latencies, 95) if latencies else 0,
                "latency_max": np.max(latencies) if latencies else 0,
                **self.system_usage(),
                "cost_per_query": 0.0
            },
            
            "grade_distribution": self._calculate_grade_distribution(successful_answers) if successful_answers else {"F": 1.0},
            "detailed_results": results,
            "rate_limit_info": {
                "limit": "3 RPM (VoyageAI free tier)",
                "solution": "Add payment method to VoyageAI dashboard"
            }
        }

        return final_results

    def _calculate_grade_distribution(self, answer_scores):
        """Calculate distribution of grades."""
        grades = [self.get_grade(a["overall_quality"]) for a in answer_scores]
        grade_counts = {grade: grades.count(grade) for grade in ["A", "B", "C", "D", "F"]}
        total = len(grades)
        return {grade: count/total for grade, count in grade_counts.items()}

    # ----------------- Results Display -----------------
    def print_results(self, results):
        """Print beautifully formatted evaluation results."""
        if not results:
            print("❌ No results to display!")
            return

        print("\n" + "="*75)
        print("🔍 RAG EVALUATION RESULTS - IMPROVED METRICS")
        print("="*75)
        print(f"Total Queries: {results['total_queries']} | Successful: {results['successful_queries']}")
        
        # Answer Quality (Most Important)
        print("\n📝 ANSWER QUALITY METRICS")
        aq = results['answer_quality']
        overall_grade = self.get_grade(aq['avg_overall_quality'])
        
        print(f"  Overall Quality:      {aq['avg_overall_quality']:.3f} ({overall_grade})")
        print(f"  Semantic Similarity:  {aq['avg_semantic_similarity']:.3f} ({self.get_grade(aq['avg_semantic_similarity'])})")
        print(f"  Faithfulness:         {aq['avg_faithfulness']:.3f}")
        print(f"  Completeness:         {aq['avg_completeness']:.3f}")
        print(f"  Relevance:            {aq['avg_relevance']:.3f}")
        print(f"  Exact Match:          {aq['avg_exact_match']:.3f}")

        # Grade Distribution
        print("\n📊 GRADE DISTRIBUTION")
        gd = results['grade_distribution']
        for grade in ["A", "B", "C", "D", "F"]:
            bar_length = int(gd[grade] * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            print(f"  {grade}: {bar} {gd[grade]*100:5.1f}%")

        # Retrieval Performance
        print("\n📥 RETRIEVAL METRICS")
        rm = results['retrieval_metrics']
        print(f"  Similarity Score:     {rm['avg_similarity_score']:.3f}")
        print(f"  Threshold Pass Rate:  {rm['threshold_pass_rate']:.3f} ({rm['threshold_pass_rate']*100:.1f}%)")
        print(f"  P@1 (improved):       {rm['avg_p_at_1']:.3f}")
        print(f"  MRR (improved):       {rm['avg_mrr']:.3f}")
        
        # Performance
        print("\n⚡ PERFORMANCE METRICS")
        perf = results['performance']
        print(f"  Latency Mean:    {perf['latency_mean']:.0f} ms")
        print(f"  Latency P50:     {perf['latency_p50']:.0f} ms")
        print(f"  Latency P95:     {perf['latency_p95']:.0f} ms")
        print(f"  Memory Usage:    {perf['memory_mb']:.1f} MB")
        print(f"  CPU Usage:       {perf['cpu_percent']:.1f}%")
        
        # Insights and Recommendations
        print("\n💡 INSIGHTS & RECOMMENDATIONS")
        self._print_recommendations(results)
        
        print("\n⭐ SUMMARY")
        print(f"  Overall Grade: {overall_grade}")
        print(f"  System Status: {self._get_system_status(results)}")
        print("="*75)

    

    def _print_recommendations(self, results):
        """Print actionable recommendations based on results."""
        aq = results['answer_quality']
        perf = results['performance']
        
        # Quality recommendations
        if aq['avg_semantic_similarity'] < 0.3:
            print("  🔴 Low semantic similarity - review your retrieval and generation pipeline")
        elif aq['avg_semantic_similarity'] < 0.5:
            print("  🟡 Moderate similarity - good foundation, room for improvement")
        else:
            print("  🟢 Good semantic similarity - answers are well-aligned!")

        # Faithfulness check
        if aq['avg_faithfulness'] < 0.4:
            print("  🔴 Low faithfulness - answers may not be grounded in retrieved content")
        elif aq['avg_faithfulness'] < aq['avg_semantic_similarity'] - 0.1:
            print("  🟡 Faithfulness lower than similarity - check citation quality")

        # Performance recommendations  
        if perf['latency_p95'] > 5000:
            print("  🐌 High latency (P95 > 5s) - consider pipeline optimization")
        elif perf['latency_p50'] > 2000:
            print("  🟡 Moderate latency - acceptable but could be improved")

        # Grade distribution insights
        gd = results['grade_distribution']
        if gd['A'] + gd['B'] > 0.6:
            print("  🎯 Strong performance - majority of answers are good quality")
        elif gd['C'] + gd['D'] + gd['F'] > 0.6:
            print("  📈 Needs improvement - majority of answers below acceptable quality")

    def _get_system_status(self, results):
        """Get overall system status."""
        overall_quality = results['answer_quality']['avg_overall_quality']
        if overall_quality >= 0.7:
            return "🟢 Excellent"
        elif overall_quality >= 0.5:
            return "🟡 Good"
        elif overall_quality >= 0.3:
            return "🟠 Needs Improvement"
        else:
            return "🔴 Poor"


    def save_results(self, results, filename="rag_evaluation_results.json"):
        """Save detailed results to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📁 Results saved to {filename}")



# ----------------- Main Execution -----------------
if __name__ == "__main__":
    # Configuration
    API_URL = "https://jioflow-insight.onrender.com"
    QUERIES_FILE = "queries.json"
    GEMINI_KEY = None  # Add your Gemini API key here if you want LLM-as-judge evaluation
    
    # Initialize evaluator
    print("🚀 Initializing RAG Evaluator...")
    evaluator = RAGEvaluator(
        api_url=API_URL,
        gemini_key=GEMINI_KEY,
        model_name="multi-qa-mpnet-base-dot-v1"
    )
    
    # Run evaluation
    print(f"📊 Starting evaluation with queries from {QUERIES_FILE}")
    results = evaluator.run_evaluation_with_3rpm_limit(QUERIES_FILE)
    
    if results:
        # Print results
        evaluator.print_results(results)
        
        # Save detailed results
        evaluator.save_results(results)
        
        # Optional: Print a few example comparisons
        print("\n🔍 SAMPLE COMPARISONS")
        print("-" * 50)
        for i, result in enumerate(results['detailed_results'][:3]):
            print(f"\nExample {i+1}:")
            print(f"Query: {result['query'][:100]}...")
            print(f"Expected: {result['expected_answer'][:100]}...")
            print(f"Generated: {result['generated_answer'][:100]}...")
            print(f"Quality: {result['answer_metrics']['overall_quality']:.3f} ({evaluator.get_grade(result['answer_metrics']['overall_quality'])})")
            print("-" * 30)
    else:
        print("❌ Evaluation failed - check your API endpoint and query file")