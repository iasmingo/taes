#!/usr/bin/env python3
"""
Script para gerar relatório textual a partir de um score_report.json existente.
Uso: python3 view_report.py [caminho_para_score_report.json]
"""

import sys
from pipeline.report_generator import generate_text_report


def main():
    # Arquivo padrão
    report_file = "data/score_report.json"
    output_file = "data/score_report.txt"
    
    # Aceitar arquivo customizado via argumento
    if len(sys.argv) > 1:
        report_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    try:
        generate_text_report(report_file, output_file)
        print(f"\n✓ Relatório gerado com sucesso!")
        print(f"  Arquivo: {output_file}")
        print(f"\nPara visualizar o relatório, execute:")
        print(f"  cat {output_file}")
        print(f"  # ou")
        print(f"  less {output_file}")
    except FileNotFoundError:
        print(f"\n✗ Erro: Arquivo '{report_file}' não encontrado.")
        print(f"  Execute primeiro: python3.9 run_pipeline.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erro ao gerar relatório: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
