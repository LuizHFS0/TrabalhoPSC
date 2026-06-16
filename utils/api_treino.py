import requests
from typing import Optional

API_KEY = "wXfTaJMnjpdtf9caRh1HVIKgnuUP1RovSAOqUW5v"
API_URL = "https://api.api-ninjas.com/v1/exercises"

OBJETIVO_TIPO = {
    "emagrecimento": "cardio",
    "hipertrofia": "strength",
    "condicionamento": "cardio",
    "força": "powerlifting",
    "flexibilidade": "stretching",
    "saúde geral": "strength",
}

NIVEL_DIFICULDADE = {
    "iniciante": "beginner",
    "intermediário": "intermediate",
    "avançado": "expert",
}

TRADUCAO_MUSCULOS = {
    "chest": "Peito",
    "back": "Costas",
    "legs": "Pernas",
    "shoulders": "Ombros",
    "biceps": "Bíceps",
    "triceps": "Tríceps",
    "abdominals": "Abdômen",
    "glutes": "Glúteos",
    "hamstrings": "Posterior de coxa",
    "quadriceps": "Quadríceps",
    "calves": "Panturrilha",
    "forearms": "Antebraço",
    "traps": "Trapézio",
    "lats": "Latíssimo",
}


def buscar_exercicios(musculo: str, dificuldade: str, tipo: Optional[str] = None, quantidade: int = 2) -> list:
    params = {"muscle": musculo, "difficulty": dificuldade}
    if tipo:
        params["type"] = tipo

    headers = {"X-Api-Key": API_KEY}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()[:quantidade]
        return []
    except requests.exceptions.RequestException:
        return []


def gerar_treino_completo(objetivo: str, nivel: str, doencas: Optional[str] = None) -> list:
    objetivo_lower = objetivo.lower() if objetivo else "saúde geral"
    nivel_lower = nivel.lower() if nivel else "iniciante"

    tipo = None
    for chave, valor in OBJETIVO_TIPO.items():
        if chave in objetivo_lower:
            tipo = valor
            break
    if not tipo:
        tipo = "strength"

    dificuldade = None
    for chave, valor in NIVEL_DIFICULDADE.items():
        if chave in nivel_lower:
            dificuldade = valor
            break
    if not dificuldade:
        dificuldade = "beginner"

    if "emagrecimento" in objetivo_lower or "condicionamento" in objetivo_lower:
        grupos = ["chest", "back", "legs", "abdominals", "shoulders"]
        series, repeticoes = 3, 15
    elif "hipertrofia" in objetivo_lower:
        grupos = ["chest", "back", "legs", "shoulders", "biceps", "triceps"]
        series, repeticoes = 4, 10
    elif "força" in objetivo_lower:
        grupos = ["chest", "back", "legs", "shoulders", "biceps", "triceps"]
        series, repeticoes = 5, 5
    else:
        grupos = ["chest", "back", "legs", "abdominals", "shoulders"]
        series, repeticoes = 3, 12

    treino = []

    for musculo in grupos:
        exercicios = buscar_exercicios(musculo, dificuldade, tipo, quantidade=2)

        if not exercicios:
            exercicios = buscar_exercicios(musculo, dificuldade, quantidade=2)

        for ex in exercicios:
            musculo_pt = TRADUCAO_MUSCULOS.get(ex.get("muscle", ""), ex.get("muscle", ""))
            treino.append({
                "nome_treino": f"Treino - {objetivo.title()}",
                "exercicio": ex.get("name", "Exercício"),
                "musculo": musculo_pt,
                "tipo": ex.get("type", ""),
                "instrucoes": ex.get("instructions", ""),
                "series": series,
                "repeticoes": repeticoes,
                "carga": None,
                "observacoes": f"Músculo: {musculo_pt} | Nível: {nivel}",
            })

    return treino
