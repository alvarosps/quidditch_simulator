from team import Team, ARTILHEIROS, BATEDORES, GOLEIRO, APANHADOR
from teams.agua import equipeAgua
from teams.ar import equipeAr
from teams.fogo import equipeFogo
from teams.terra import equipeTerra
from teams.pdc import equipePDC
from teams.castelobruxo import equipeCasteloBruxo
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
        
    rodada = 1
    team_1_bonus = {
        ARTILHEIROS: 0,
        BATEDORES: 0,
        GOLEIRO: 0,
        APANHADOR: 0
    }
    team_2_bonus = {
        ARTILHEIROS: 0,
        BATEDORES: 0,
        GOLEIRO: 0,
        APANHADOR: 0
    }
    
    team_1_restantes = {
        ARTILHEIROS: 6,
        BATEDORES: 4,
        GOLEIRO: 2,
        APANHADOR: 2
    }
    team_2_restantes = {
        ARTILHEIROS: 6,
        BATEDORES: 4,
        GOLEIRO: 2,
        APANHADOR: 2
    }
    
    incluir_score_inicial_choice = input("Deseja inserir dados iniciais? (1 para sim, 0 para não):\t")
    incluir_score_inicial = False
    if incluir_score_inicial_choice == '1':
        incluir_score_inicial = True
    if incluir_score_inicial == True:
        team1_score_inicial = int(input(f"\n\tScore inicial da equipe {team_1.name}:\t"))
        team_1_bonus_artilheiros = int(input(f"\tBonus inicial dos artilheiros da {team_1.name}:\t"))
        team_1_bonus_batedores = int(input(f"\tBonus inicial dos batedores da {team_1.name}:\t"))
        team_1_bonus_goleiro = int(input(f"\tBonus inicial do goleiro da {team_1.name}:\t"))
        team_1_bonus_apanhador = int(input(f"\tBonus inicial do apanhador da {team_1.name}:\t"))
        team_1_bonus = {
            ARTILHEIROS: team_1_bonus_artilheiros,
            BATEDORES: team_1_bonus_batedores,
            GOLEIRO: team_1_bonus_goleiro,
            APANHADOR: team_1_bonus_apanhador
        }
        # Sobre substituicoes, ajusta o numero de restantes, mas tem que trocar o time manualmente
        print(f"\tTeve substituições no time {team_1.name}?")
        print("\t1 - Sim")
        print("\t0 - Não")
        team_1_substituicoes = int(input("\tResposta:\t"))
        if team_1_substituicoes == 1:
            team_1_substituicoes_artilheiros = int(input("\t\tTeve substituições de artilheiros? quantas?\t"))
            team_1_restantes[ARTILHEIROS] -= team_1_substituicoes_artilheiros
            team_1_substituicoes_batedores = int(input("\t\tTeve substituições de batedores? quantas?\t"))
            team_1_restantes[BATEDORES] -= team_1_substituicoes_batedores
            team_1_substituicoes_goleiro = int(input("\t\tTeve substituições de goleiro? quantas?\t"))
            team_1_restantes[GOLEIRO] -= team_1_substituicoes_goleiro
            team_1_substituicoes_apanhador = int(input("\t\tTeve substituições de apanhador? quantas?\t"))
            team_1_restantes[APANHADOR] -= team_1_substituicoes_apanhador
        
        
        team_1.set_initial_score(team1_score_inicial)
        team_1.set_crowd_bonus_next_round(team_1_bonus)
        team_1.set_players_remaining(team_1_restantes)
        
        team2_score_inicial = int(input(f"\n\tScore inicial da equipe {team_2.name}:\t"))
        team_2_bonus_artilheiros = int(input(f"\tBonus inicial dos artilheiros da {team_2.name}:\t"))
        team_2_bonus_batedores = int(input(f"\tBonus inicial dos batedores da {team_2.name}:\t"))
        team_2_bonus_goleiro = int(input(f"\tBonus inicial do goleiro da {team_2.name}:\t"))
        team_2_bonus_apanhador = int(input(f"\tBonus inicial do apanhador da {team_2.name}:\t"))
        team_2_bonus = {
            ARTILHEIROS: team_2_bonus_artilheiros,
            BATEDORES: team_2_bonus_batedores,
            GOLEIRO: team_2_bonus_goleiro,
            APANHADOR: team_2_bonus_apanhador
        }
        # Sobre substituicoes, ajusta o numero de restantes, mas tem que trocar o time manualmente
        print(f"\tTeve substituições no time {team_2.name}?")
        print("\t1 - Sim")
        print("\t0 - Não")
        team_2_substituicoes = int(input("\tResposta:\t"))
        if team_2_substituicoes == 1:
            team_2_substituicoes_artilheiros = int(input("\t\tTeve substituições de artilheiros? quantas?\t"))
            team_2_restantes[ARTILHEIROS] -= team_2_substituicoes_artilheiros
            team_2_substituicoes_batedores = int(input("\t\tTeve substituições de batedores? quantas?\t"))
            team_2_restantes[BATEDORES] -= team_2_substituicoes_batedores
            team_2_substituicoes_goleiro = int(input("\t\tTeve substituições de goleiro? quantas?\t"))
            team_2_restantes[GOLEIRO] -= team_2_substituicoes_goleiro
            team_2_substituicoes_apanhador = int(input("\t\tTeve substituições de apanhador? quantas?\t"))
            team_2_restantes[APANHADOR] -= team_2_substituicoes_apanhador
        team_2.set_initial_score(team2_score_inicial)
        team_2.set_crowd_bonus_next_round(team_2_bonus)
        team_2.set_players_remaining(team_2_restantes)
        rodada = int(input("\n\tRodada inicial (1+):\t"))

    simulate_game(team_1, team_2, rodada, automate_game)

if __name__ == '__main__':
    main()

