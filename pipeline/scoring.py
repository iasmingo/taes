"""
Sistema de scoring determinístico para verificação de diagramas UML.
Define pesos e calcula scores baseado nos erros identificados pela IA.
"""

# Pesos por tipo de erro (0-100, quanto maior o peso, mais grave)
ERROR_WEIGHTS = {
    # Erros críticos (25-30 pontos) - elementos fundamentais faltando
    "missing_actor": 30,
    "missing_entity": 30,
    "missing_participant": 28,
    
    # Erros graves (15-24 pontos) - elementos extras ou mapeamentos incorretos
    "extra_actor": 18,
    "extra_class": 18,
    "extra_participant": 18,
    "missing_usecase": 22,
    "missing_method": 22,
    "missing_message": 20,
    
    # Erros médios (10-14 pontos) - relações e mapeamentos
    "missing_relation": 15,
    "usecase_not_mapped": 12,
    "method_without_usecase": 12,
    "lifeline_without_class": 14,
    "message_without_method": 14,
    
    # Erros leves (5-9 pontos) - problemas de fluxo e ordem
    "extra_usecase": 8,
    "wrong_message_order": 7,
    "incompatible_flow": 9
}

# Peso de cada seção na nota final
SECTION_WEIGHTS = {
    "json_vs_usecase": 0.20,      # 20%
    "json_vs_classes": 0.25,      # 25%
    "json_vs_sequence": 0.20,     # 20%
    "usecase_vs_classes": 0.15,   # 15%
    "classes_vs_sequence": 0.20   # 20%
}


def calculate_section_score(section_data):
    """
    Calcula o score de uma seção baseado nos erros encontrados.
    
    Returns:
        dict com score, penalidades e estatísticas
    """
    if section_data["status"] == "OK":
        return {
            "score": 100.0,
            "total_penalty": 0,
            "error_count": 0,
            "coverage": 100.0
        }
    
    errors = section_data.get("errors", [])
    counts = section_data.get("counts", {})
    
    # 1. Calcular penalidade por erros (máximo 80 pontos)
    total_penalty = 0
    error_breakdown = {}
    
    for error in errors:
        error_type = error.get("type", "unknown")
        weight = ERROR_WEIGHTS.get(error_type, 15)  # default 15
        total_penalty += weight
        
        if error_type not in error_breakdown:
            error_breakdown[error_type] = {"count": 0, "penalty": 0}
        error_breakdown[error_type]["count"] += 1
        error_breakdown[error_type]["penalty"] += weight
    
    # Limitar penalidade máxima a 70 (mínimo score = 30)
    total_penalty = min(total_penalty, 70)
    
    # 2. Calcular cobertura (baseado nas contagens)
    coverage = calculate_coverage(counts)
    
    # 3. Score final = 100 - penalidade + bônus de cobertura parcial
    coverage_bonus = (coverage / 100) * 15  # máximo 15 pontos de bônus
    base_score = 100 - total_penalty
    final_score = max(30, min(100, base_score + coverage_bonus))
    
    return {
        "score": round(final_score, 2),
        "total_penalty": total_penalty,
        "error_count": len(errors),
        "coverage": round(coverage, 2),
        "error_breakdown": error_breakdown
    }


def calculate_coverage(counts):
    """
    Calcula porcentagem de cobertura baseado nas contagens.
    """
    if not counts:
        return 100.0
    
    # Identificar pares de total/encontrado
    coverage_pairs = []
    
    # Padrões comuns: total_X / found_X ou X_expected / X_found
    for key, value in counts.items():
        if key.startswith("total_"):
            found_key = key.replace("total_", "found_")
            if found_key in counts:
                total = value
                found = counts[found_key]
                if total > 0:
                    coverage_pairs.append(found / total * 100)
        
        elif key.endswith("_expected"):
            found_key = key.replace("_expected", "_found")
            if found_key in counts:
                total = value
                found = counts[found_key]
                if total > 0:
                    coverage_pairs.append(found / total * 100)
    
    # Se não encontrou pares, tentar outras combinações
    if not coverage_pairs:
        # Exemplo: total_actors_json / found_actors_usecase
        if "total_actors_json" in counts and "found_actors_usecase" in counts:
            total = counts["total_actors_json"]
            found = counts["found_actors_usecase"]
            if total > 0:
                coverage_pairs.append(found / total * 100)
        
        if "total_entities_json" in counts and "found_classes" in counts:
            total = counts["total_entities_json"]
            found = counts["found_classes"]
            if total > 0:
                coverage_pairs.append(found / total * 100)
    
    # Retornar média das coberturas
    if coverage_pairs:
        return sum(coverage_pairs) / len(coverage_pairs)
    
    return 100.0


def calculate_overall_score(verification_result):
    """
    Calcula o score geral ponderado de todas as seções.
    
    Args:
        verification_result: JSON retornado pela IA
        
    Returns:
        dict com scores detalhados e nota final
    """
    section_scores = {}
    
    # Calcular score de cada seção
    for section_name, section_weight in SECTION_WEIGHTS.items():
        if section_name in verification_result:
            section_data = verification_result[section_name]
            section_result = calculate_section_score(section_data)
            section_result["weight"] = section_weight
            section_scores[section_name] = section_result
    
    # Calcular score geral ponderado
    weighted_sum = sum(
        scores["score"] * scores["weight"]
        for scores in section_scores.values()
    )
    
    overall_score = round(weighted_sum, 2)
    
    # Determinar nota (A-F)
    grade = get_grade(overall_score)
    
    # Estatísticas gerais
    total_errors = sum(s["error_count"] for s in section_scores.values())
    total_penalty = sum(s["total_penalty"] for s in section_scores.values())
    avg_coverage = sum(s["coverage"] for s in section_scores.values()) / len(section_scores)
    
    return {
        "overall_score": overall_score,
        "grade": grade,
        "section_scores": section_scores,
        "summary": {
            "total_errors": total_errors,
            "total_penalty": round(total_penalty, 2),
            "average_coverage": round(avg_coverage, 2),
            "passed": overall_score >= 60.0
        }
    }


def get_grade(score):
    """Converte score numérico em nota alfabética."""
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    if score >= 60: return "D"
    return "F"


def generate_report(verification_result, output_file="data/score_report.json"):
    """
    Gera relatório completo com scores e salva em arquivo.
    """
    scoring_result = calculate_overall_score(verification_result)
    
    # Adicionar informações originais da verificação
    report = {
        "scoring": scoring_result,
        "verification": verification_result,
        "config": {
            "error_weights": ERROR_WEIGHTS,
            "section_weights": SECTION_WEIGHTS
        }
    }
    
    import json
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, indent=2, ensure_ascii=False, fp=f)
    
    # Print resumo no console
    print("\n" + "="*60)
    print("RELATÓRIO DE SCORING")
    print("="*60)
    print(f"Score Geral: {scoring_result['overall_score']}/100 - Nota: {scoring_result['grade']}")
    print(f"Total de Erros: {scoring_result['summary']['total_errors']}")
    print(f"Cobertura Média: {scoring_result['summary']['average_coverage']}%")
    print(f"Status: {'✓ APROVADO' if scoring_result['summary']['passed'] else '✗ REPROVADO'}")
    print("\nScores por Seção:")
    for section, data in scoring_result['section_scores'].items():
        print(f"  {section}: {data['score']}/100 ({data['error_count']} erros)")
    print("="*60 + "\n")
    
    # Gerar relatório textual detalhado
    try:
        from report_generator import generate_text_report
        generate_text_report(output_file, "data/score_report.txt")
    except Exception as e:
        print(f"⚠ Erro ao gerar relatório textual: {e}")
    
    return report
