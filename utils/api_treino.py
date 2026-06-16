import random
import requests
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ZYLA_API_KEY", "")
BASE_URL = "https://zylalabs.com/api/392/exercise+database+api"

# Musculos no formato que a Zyla aceita como "target"
OBJETIVO_MUSCULOS = {
    "emagrecimento":    ["abs", "quads", "glutes", "hamstrings", "cardiovascular system"],
    "condicionamento":  ["abs", "quads", "glutes", "hamstrings", "cardiovascular system"],
    "hipertrofia":      ["pectorals", "lats", "biceps", "triceps", "delts", "quads"],
    "força":            ["pectorals", "lats", "biceps", "triceps", "delts", "quads"],
    "flexibilidade":    ["abs", "glutes", "hamstrings", "spine", "adductors"],
    "saúde geral":      ["pectorals", "lats", "abs", "quads", "delts"],
}

OBJETIVO_SERIES_REPS = {
    "emagrecimento":   (3, 15),
    "condicionamento": (3, 15),
    "hipertrofia":     (4, 10),
    "força":           (5, 5),
    "flexibilidade":   (3, 12),
    "saúde geral":     (3, 12),
}

TRADUCAO_MUSCULOS = {
    "abs":                  "Abdômen",
    "quads":                "Quadríceps",
    "lats":                 "Latíssimo",
    "calves":               "Panturrilha",
    "pectorals":            "Peito",
    "glutes":               "Glúteos",
    "hamstrings":           "Posterior de coxa",
    "adductors":            "Adutores",
    "triceps":              "Tríceps",
    "cardiovascular system":"Cardiovascular",
    "spine":                "Coluna",
    "upper back":           "Costas superiores",
    "biceps":               "Bíceps",
    "delts":                "Deltóide",
    "forearms":             "Antebraço",
    "traps":                "Trapézio",
    "serratus anterior":    "Serrátil anterior",
    "abductors":            "Abdutores",
    "levator scapulae":     "Elevador da escápula",
}


def _buscar_por_musculo(target: str, quantidade: int = 3) -> list:
    """Busca exercícios pelo músculo alvo na Zyla Exercise Database."""
    url = f"{BASE_URL}/312/list+by+target+muscle"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"target": target}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"[API] target={target} status={response.status_code}")

        if response.status_code == 200:
            exercicios = response.json()
            if exercicios:
                # Embaralha para variar o treino a cada geração
                random.shuffle(exercicios)
                return exercicios[:quantidade]
        else:
            print(f"[API] Erro: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"[API] Erro de conexão: {e}")

    return []


def gerar_treino_completo(objetivo: str, nivel: str, doencas: Optional[str] = None) -> list:
    objetivo_lower = objetivo.lower() if objetivo else "saúde geral"

    # Detecta qual chave de objetivo usar
    chave_objetivo = "saúde geral"
    for chave in OBJETIVO_MUSCULOS:
        if chave in objetivo_lower:
            chave_objetivo = chave
            break

    musculos = OBJETIVO_MUSCULOS[chave_objetivo]
    series, repeticoes = OBJETIVO_SERIES_REPS[chave_objetivo]
    nome_treino = f"Treino - {objetivo.title()}"

    treino = []

    for musculo in musculos:
        exercicios = _buscar_por_musculo(musculo, quantidade=2)
        print(f"[TREINO] musculo={musculo} → {len(exercicios)} exercício(s)")

        for ex in exercicios:
            musculo_pt = TRADUCAO_MUSCULOS.get(ex.get("target", ""), ex.get("target", ""))
            treino.append({
                "nome_treino":  nome_treino,
                "exercicio":    ex.get("name", "Exercício").title(),
                "musculo":      musculo_pt,
                "series":       series,
                "repeticoes":   repeticoes,
                "carga":        None,
                "observacoes":  f"Músculo: {musculo_pt} | Equipamento: {ex.get('equipment', '—')} | Nível: {nivel}",
            })

    print(f"[TREINO] Total gerado: {len(treino)} exercícios")

    if not treino:
        print("[TREINO] API vazia — usando treino de fallback")
        return _treino_fallback(objetivo, nivel)

    return treino


def _treino_fallback(objetivo: str, nivel: str) -> list:
    """Treino padrão caso a API não retorne dados."""
    nome = f"Treino - {objetivo.title()}"
    return [
        {"nome_treino": nome, "exercicio": "Supino Reto",      "musculo": "Peito",      "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
        {"nome_treino": nome, "exercicio": "Agachamento",       "musculo": "Quadríceps", "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
        {"nome_treino": nome, "exercicio": "Remada Curvada",    "musculo": "Costas",     "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
        {"nome_treino": nome, "exercicio": "Desenvolvimento",   "musculo": "Deltóide",   "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
        {"nome_treino": nome, "exercicio": "Rosca Direta",      "musculo": "Bíceps",     "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
        {"nome_treino": nome, "exercicio": "Tríceps Pulley",    "musculo": "Tríceps",    "series": 3, "repeticoes": 12, "carga": None, "observacoes": f"Nível: {nivel}"},
    ]