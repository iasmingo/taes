"""
Módulo de geração de relatório textual para os scores de verificação UML.
Gera um relatório em texto simples, claro e bem formatado.
"""

import json
from datetime import datetime


def generate_text_report(score_report_path, output_path="data/score_report.txt"):
    """
    Gera um relatório textual detalhado a partir do score_report.json.
    
    Args:
        score_report_path: Caminho para o arquivo score_report.json
        output_path: Caminho onde salvar o relatório .txt
    """
    # Carregar dados
    with open(score_report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    scoring = report['scoring']
    config = report['config']
    verification = report['verification']
    
    # Gerar relatório
    lines = []
    
    # Cabeçalho
    lines.append("=" * 80)
    lines.append("RELATÓRIO DE VERIFICAÇÃO DE CONSISTÊNCIA - DIAGRAMAS UML")
    lines.append("=" * 80)
    lines.append(f"Data de Geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append("")
    
    # Seção 1: Explicação do Sistema de Scoring
    lines.append("─" * 80)
    lines.append("1. COMO FUNCIONA O SISTEMA DE SCORING")
    lines.append("─" * 80)
    lines.append("")
    lines.append("O sistema avalia a consistência entre os diagramas UML gerados pela IA,")
    lines.append("verificando se os elementos de um artefato estão corretamente representados")
    lines.append("em outros artefatos relacionados.")
    lines.append("")
    lines.append("METODOLOGIA:")
    lines.append("")
    lines.append("1. A IA identifica inconsistências entre os diagramas e as categoriza por tipo")
    lines.append("2. Cada tipo de erro recebe uma penalidade baseada em sua severidade")
    lines.append("3. O score de cada seção é calculado: 100 - penalidade total")
    lines.append("4. Um bônus de cobertura parcial pode compensar alguns erros")
    lines.append("5. O score final é uma média ponderada de todas as seções")
    lines.append("")
    lines.append("FÓRMULA DE CÁLCULO POR SEÇÃO:")
    lines.append("")
    lines.append("  1. Soma das Penalidades:")
    lines.append("     penalidade_total = Σ (peso_do_erro × quantidade)")
    lines.append("     • Penalidade máxima limitada a 70 pontos")
    lines.append("")
    lines.append("  2. Score Base:")
    lines.append("     score_base = 100 - penalidade_total")
    lines.append("")
    lines.append("  3. Bônus de Cobertura:")
    lines.append("     bonus = (cobertura% / 100) × 15")
    lines.append("     • Cobertura = % de elementos encontrados vs. esperados")
    lines.append("     • Bônus máximo: 15 pontos")
    lines.append("")
    lines.append("  4. Score Final da Seção:")
    lines.append("     score_seção = max(30, min(100, score_base + bonus))")
    lines.append("     • Mínimo: 30 pontos")
    lines.append("     • Máximo: 100 pontos")
    lines.append("")
    lines.append("FÓRMULA DO SCORE GERAL:")
    lines.append("")
    lines.append("  score_geral = Σ (score_seção × peso_seção)")
    lines.append("")
    lines.append("  Exemplo:")
    lines.append("    = (json_vs_usecase × 0.20)")
    lines.append("    + (json_vs_classes × 0.25)")
    lines.append("    + (json_vs_sequence × 0.20)")
    lines.append("    + (usecase_vs_classes × 0.15)")
    lines.append("    + (classes_vs_sequence × 0.20)")
    lines.append("")
    lines.append("NOTAS:")
    lines.append("  A (90-100) | B (80-89) | C (70-79) | D (60-69) | F (0-59)")
    lines.append("  Aprovação: Score ≥ 60.0")
    lines.append("")
    
    # Seção 2: Pesos dos Erros
    lines.append("─" * 80)
    lines.append("2. PESOS POR TIPO DE ERRO")
    lines.append("─" * 80)
    lines.append("")
    lines.append("ERROS CRÍTICOS (25-30 pontos) - Elementos fundamentais faltando:")
    critical_errors = {k: v for k, v in config['error_weights'].items() if v >= 25}
    for error_type, weight in sorted(critical_errors.items(), key=lambda x: -x[1]):
        lines.append(f"  • {error_type:.<50} {weight} pts")
    lines.append("")
    
    lines.append("ERROS GRAVES (15-24 pontos) - Mapeamentos incorretos:")
    high_errors = {k: v for k, v in config['error_weights'].items() if 15 <= v < 25}
    for error_type, weight in sorted(high_errors.items(), key=lambda x: -x[1]):
        lines.append(f"  • {error_type:.<50} {weight} pts")
    lines.append("")
    
    lines.append("ERROS MÉDIOS (10-14 pontos) - Relações e estruturas:")
    medium_errors = {k: v for k, v in config['error_weights'].items() if 10 <= v < 15}
    for error_type, weight in sorted(medium_errors.items(), key=lambda x: -x[1]):
        lines.append(f"  • {error_type:.<50} {weight} pts")
    lines.append("")
    
    lines.append("ERROS LEVES (5-9 pontos) - Problemas de fluxo:")
    low_errors = {k: v for k, v in config['error_weights'].items() if 5 <= v < 10}
    if low_errors:
        for error_type, weight in sorted(low_errors.items(), key=lambda x: -x[1]):
            lines.append(f"  • {error_type:.<50} {weight} pts")
    else:
        lines.append("  (Nenhum erro leve definido no sistema)")
    lines.append("")
    
    # Seção 3: Pesos das Seções
    lines.append("─" * 80)
    lines.append("3. PESO DE CADA SEÇÃO NA AVALIAÇÃO FINAL")
    lines.append("─" * 80)
    lines.append("")
    section_names = {
        'json_vs_usecase': 'JSON ↔ Diagrama de Casos de Uso',
        'json_vs_classes': 'JSON ↔ Diagrama de Classes',
        'json_vs_sequence': 'JSON ↔ Diagrama de Sequência',
        'usecase_vs_classes': 'Casos de Uso ↔ Classes',
        'classes_vs_sequence': 'Classes ↔ Sequência'
    }
    for section, weight in config['section_weights'].items():
        section_name = section_names.get(section, section)
        percentage = weight * 100
        bar = "█" * int(percentage / 5)
        lines.append(f"  {section_name:.<45} {percentage:>5.0f}% {bar}")
    lines.append("")
    
    # Seção 4: Resultado Geral
    lines.append("=" * 80)
    lines.append("4. RESULTADO GERAL DA AVALIAÇÃO")
    lines.append("=" * 80)
    lines.append("")
    
    overall_score = scoring['overall_score']
    grade = scoring['grade']
    passed = scoring['summary']['passed']
    
    # Desenhar barra de score
    score_bar_length = int(overall_score / 2.5)
    score_bar = "█" * score_bar_length
    empty_bar = "░" * (40 - score_bar_length)
    
    lines.append(f"  SCORE FINAL: {overall_score:.2f}/100")
    lines.append(f"  [{score_bar}{empty_bar}]")
    lines.append(f"  NOTA: {grade}")
    lines.append(f"  STATUS: {'✓ APROVADO' if passed else '✗ REPROVADO'} (mínimo: 60.0)")
    lines.append("")
    
    lines.append("ESTATÍSTICAS:")
    lines.append(f"  • Total de Erros Encontrados: {scoring['summary']['total_errors']}")
    lines.append(f"  • Penalidade Total Aplicada: {scoring['summary']['total_penalty']:.2f} pontos")
    lines.append(f"  • Cobertura Média: {scoring['summary']['average_coverage']:.2f}%")
    lines.append("")
    
    # Seção 5: Desempenho por Seção
    lines.append("─" * 80)
    lines.append("5. DESEMPENHO DETALHADO POR SEÇÃO")
    lines.append("─" * 80)
    lines.append("")
    
    for section, data in scoring['section_scores'].items():
        section_name = section_names.get(section, section)
        score = data['score']
        errors = data['error_count']
        coverage = data['coverage']
        weight = data['weight'] * 100
        
        # Indicador visual do score
        if score >= 90:
            status = "EXCELENTE ✓✓✓"
        elif score >= 80:
            status = "BOM ✓✓"
        elif score >= 70:
            status = "SATISFATÓRIO ✓"
        elif score >= 60:
            status = "MÍNIMO ~"
        else:
            status = "INSUFICIENTE ✗"
        
        lines.append(f"┌─ {section_name}")
        lines.append(f"│")
        lines.append(f"│  Score: {score:.2f}/100  [{status}]")
        lines.append(f"│  Erros Encontrados: {errors}")
        lines.append(f"│  Cobertura: {coverage:.2f}%")
        lines.append(f"│  Peso na Nota Final: {weight:.0f}%")
        
        # Mostrar breakdown de erros se existir
        if 'error_breakdown' in data and data['error_breakdown']:
            lines.append(f"│")
            lines.append(f"│  Detalhamento dos Erros:")
            for error_type, error_info in data['error_breakdown'].items():
                count = error_info['count']
                penalty = error_info['penalty']
                lines.append(f"│    • {error_type}: {count}x (-{penalty} pts)")
        
        lines.append(f"└{'─' * 78}")
        lines.append("")
    
    # Seção 6: Erros Identificados pela IA
    lines.append("─" * 80)
    lines.append("6. ERROS IDENTIFICADOS PELA IA")
    lines.append("─" * 80)
    lines.append("")
    
    has_errors = False
    for section, data in verification.items():
        if section == 'overall_status':
            continue
        
        section_name = section_names.get(section, section)
        section_data = data
        
        if section_data.get('status') == 'ERROR' and section_data.get('errors'):
            has_errors = True
            lines.append(f"▼ {section_name}")
            lines.append("")
            
            for i, error in enumerate(section_data['errors'], 1):
                error_type = error.get('type', 'unknown')
                element = error.get('element', 'N/A')
                details = error.get('details', 'Sem detalhes')
                weight = config['error_weights'].get(error_type, 15)
                
                lines.append(f"  {i}. Tipo: {error_type} (-{weight} pts)")
                lines.append(f"     Elemento: {element}")
                lines.append(f"     Detalhes: {details}")
                lines.append("")
            
            lines.append("")
    
    if not has_errors:
        lines.append("  ✓ Nenhum erro encontrado! Todos os diagramas estão consistentes.")
        lines.append("")
    
    # Seção 7: Conclusão
    lines.append("=" * 80)
    lines.append("7. CONCLUSÃO")
    lines.append("=" * 80)
    lines.append("")
    
    if overall_score >= 90:
        conclusion = "A IA teve um desempenho EXCELENTE na geração dos diagramas UML.\nTodos os artefatos estão altamente consistentes entre si."
    elif overall_score >= 80:
        conclusion = "A IA teve um BOM desempenho na geração dos diagramas UML.\nA maioria dos elementos está corretamente representada."
    elif overall_score >= 70:
        conclusion = "A IA teve um desempenho SATISFATÓRIO na geração dos diagramas.\nExistem algumas inconsistências que podem ser corrigidas."
    elif overall_score >= 60:
        conclusion = "A IA atingiu o desempenho MÍNIMO aceitável.\nVárias inconsistências foram encontradas e devem ser revisadas."
    else:
        conclusion = "A IA teve um desempenho INSUFICIENTE na geração dos diagramas.\nMuitas inconsistências críticas foram encontradas."
    
    lines.append(conclusion)
    lines.append("")
    
    if scoring['summary']['total_errors'] > 0:
        lines.append("RECOMENDAÇÕES:")
        lines.append("  • Revisar os erros listados na seção 6")
        lines.append("  • Ajustar os prompts da IA para melhorar a consistência")
        lines.append("  • Focar nas seções com scores mais baixos")
        lines.append("")
    
    lines.append("=" * 80)
    lines.append("FIM DO RELATÓRIO")
    lines.append("=" * 80)
    
    # Salvar arquivo
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✓ Relatório textual salvo em: {output_path}")
    
    return output_path
