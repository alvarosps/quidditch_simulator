* **CasteloBruxo Quidditch**

* Teams: Each quidditch team has the following players:
	* Main team:
		3 Chasers
		2 Beaters
		1 Keeper
		1 Seeker
	* Reserve team:
		3 Chasers
		2 Beaters
		1 Keeper
		1 Seeker

* Rules: Quidditch is a game played in turns, each turn has 5 phases, in the following order:
1. Chasers
2. Beaters
3. Keeper
4. Seeker
5. Fan inspiration

* Each quidditch player rolls 2d6 + player modifier in it's turn in the game turn. The result will be compared to this values:
	* 15 or higher (15+) -> For seekers only, considered greater success and can catch the golden snitch.
	* Between 10 and 14 (10~14) -> For seekers only, considered a success.
	* 13 or higher (13+) -> Considered a greater success (except seekers).
	* Between 10 and 12 (10+) -> Considered a success (except seekers).
	* Between 7 and 9 (7~9) -> Considered a partial success.
	* 6 or less (6-) -> Considered a failure.

* Match Turn: Each team player category will roll "at the same time". So for example, in the Keeper's turn, Keeper of Team A will roll, and Keeper of Team B will roll, and the results will be added to the game.
	* Chasers - Each chaser has it's own roll in the turn
		* 13+ : +30 points
		* 10+ : +20 points
		* 7~9 : +10 points
		* 6-  : +10 points
	* Beaters - Each beater has it's own roll in the turn
		* 13+   : +10 points
			* On the 13+ roll, the beater knocks one of the adversary team players, with this rules:
				* If manual inputs mode is enabled, user chooses
				* If ít's automatically, it randomly chooses the position that will be knocked out.
		* 10+   : +10 points
		* 7~9   : Nothing happens
		* 6-    : +10 points to adversary
	* Keeper
		* 13+ :  +10 points and -20 points to adversary
		* 10+ : +10 points and -10 points to adversary
		* 7~9 : -10 points to adversary
		* 6-  : +10 points to adversary
	* Seeker
		* Firstly, the seekers need to spot the snitch. For that, they will roll the 2d6 + modifier and check if it's a 10+. If any of the choosers rolls 10+, the snitch has been spotted, and on the next turn the seekers will be able to try to catch it. If none of the seekers rolls 10+, they'll keep trying to spot the snitch on the next turn, and it will go like that until the snitch has been spotted by one of the seekers.
		* While the other quidditch players doesn't have an order, the Seekers will have an order to roll in it's turn:
			* The order is defined by who rolled the highest roll in the last turn.
			* If the seekers had the same roll, the seeker with highest turn modifier for the next roll (modifier + forward + crowd bonus) will have the priority.
			* If the turn modifiers for each are the same, then it'll compare the players modifiers only and determine priority.
			* If the modifiers are equal, or if it's the first seeker's turn in the game, the priority will be randomly decided before the turn begins.
			* If one seeker is knocked out and the team's reserve seeker enters the game, the priority will be given to the other seeker, even if the knocked out seeker had a priority defined.
		* After the Snitch has been spotted, the following rules applies:
			* 15+ 
				* If the seeker's team is winning the game score, or if the seeker's team score difference to the adversary team is less than 50 (the snitch catching bonus), the seeker catches the golden snitch and it's team wins the game.
				* If the seeker's team is loosing the game by 50 or more points, it won't catch the snitch, but it'll get +3 forward on the next roll and priority on the next turn. However, if the other seeker rolls 15+ in this turn, it'll catch the golden snitch and wins the game.
			* 10~14 : +2 forward on next turn
			* 7~9   : +1 forward on next turn
			* 6-    : -2 forward on next turn
	* Fan Inspire
		* 10+   : Inspire person Choose 2 from the Positions to give +1 bonus for the next turn.
		* 7~9   : Inspire person Choose 1 from the Positions to give +1 bonus for the next turn.
		* 6-    : -2 bonus to randomly selected position for the next turn.
		* How they choose: Users can choose manually, if manual inputs option is enabled. Otherwise, it'll be chosen randomly, the same for the knockdown rules.
* Knockdown and Crowd bonus: How random selections work in the game:
1. If manual input mode is enabled, user chooses the priority.
2. If it's in automatic mode, the priority is: Seeker, Chaser, Beater, Keeper
	* Rolls 1d5, and the result will choose the position that will have the effect, based on:
		* Default
		1. Keeper
		2. Beater
		3. Chaser
		4. Seeker
		5. Seeker
		* If one of the positions doesn't have more players in the match, the priority position will assume it's possibility in the turn, example, if there isn't a Keeper in the game anymore:
		1. Seeker
		2. Beater
		3. Chaser
		4. Seeker
		5. Seeker
		* And, if the first priority position is not in the game anymore, it'll move to the next position. For example, if the team doesn't have a Seeker anymore, it'll be:
		1. Keeper
		2. Beater
		3. Chaser
		4. Chaser
		5. Chaser
3. Knockdown specific rules:
	* When a player is knocked down, they are out of the match. If there is a reserve player in the same position available, that player will join the match. If there isn't a player in the same position available in the reserve team, the knocked out player team will have a player less than the other team.
	* If there isn't any player available in a given position for the team, that team's position turn will be skipped and only the other team's position will have it's turn.
	* If there isn't any seeker in the match, match ends.
	* If there is 1 seeker in the match, it can still catch the snitch and win the match. But if there are more than 10 match turns and the seeker decided not to catch the snitch (because it's team is loosing the match by a large amount, probably), the match will end.

* Quidditch Players: Each quidditch player has the following attributes:
1. Name
2. House (Terra, Fogo, Água ou Ar) - Necessary because player can be chosen for the school's team. Optional argument because a quidditch player can be from other 
2. Modifier (if it's an NPC, will be a GM determined modifier (that represents the player's position modifier, if it's a player, it'll be that position modifier)
	* Chaser - Heart
	* Beater - Body
	* Keeper - Soul
	* Seeker - Mind
3. Crowd Bonus
	* Default: 0
	* It's modified the Fan Inspire turn, if the player position was chosen
4. Forward (Optional - seekers only)
	* Default: 0
	* It's modified on each turn, depending on the seeker's roll.
	* When game ends should be set to default.
5. Round Bonus (Optional - Seekers only)
	* Default: 0
	* It's incremented on each turn by 1
	* When game ends, should be set to default.
