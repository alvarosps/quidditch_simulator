from team import Team
from teams import equipeAgua, equipeAr, equipeCasteloBruxo, equipeFogo, equipePDC, equipeTerra
from utils import simulate_game, select_team

teamAgua = Team(equipeAgua['nome'], equipeAgua['equipe'], equipeAgua['torcida'])
teamAr = Team(equipeAr['nome'], equipeAr['equipe'], equipeAr['torcida'])
teamFogo = Team(equipeFogo['nome'], equipeFogo['equipe'], equipeFogo['torcida'])
teamTerra = Team(equipeTerra['nome'], equipeTerra['equipe'], equipeTerra['torcida'])
teamCastelobruxo = Team(equipeCasteloBruxo['nome'], equipeCasteloBruxo['equipe'], equipeCasteloBruxo['torcida'])
teamPDC = Team(equipePDC['nome'], equipePDC['equipe'], equipePDC['torcida'])

teams = {
    'Agua': teamAgua,
    'Ar': teamAr,
    'Fogo': teamFogo,
    'Terra': teamTerra,
    'Castelobruxo': teamCastelobruxo,
    'PDC': teamPDC
}

def main():
    print("Escolha o primeiro time a jogar: ")
    opcoes = ["Agua", "Ar", "Fogo", "Terra", "Castelobruxo", "PDC"]
    team_1 = teams[select_team(opcoes)]
    print(f"Time {team_1.name} escolhido")

    print("Escolhe o segundo time a jogar: ")
    team_2 = teams[select_team(opcoes)]
    print(f"Time {team_2.name} escolhido")
    
    automate_game_choice = input("Deseja jogo automatizado (sem input de usuario)? (1 para sim, 0 para não): ")
    automate_game = False
    if automate_game_choice == '1':
        automate_game = True

    incluir_score_inicial_choice = input("Deseja inserir scores iniciais? (1 para sim, 0 para não): ")
    incluir_score_inicial = False
    if incluir_score_inicial_choice == '1':
        incluir_score_inicial = True
    if incluir_score_inicial == True:
        team1_score_inicial = int(input(f"Score inicial da equipe {team_1.name}: "))
        team_1.set_initial_score(team1_score_inicial)
        team2_score_inicial = int(input(f"Score inicial da equipe {team_2.name}:"))
        team_2.set_initial_score(team2_score_inicial)

    simulate_game(team_1, team_2, automate_game)

if __name__ == '__main__':
    main()

