

Cards have an activate method

activate(current_state) -> new_state | None

if None the card is not playable
else the card returns the new state

States are complicated

future state are binaries (or more ) with probabilites attached to them depending on the dice rolls and thus sthe success of failure of the card / crafter combination. On top of that, criticals and failure can activate other cards or change state (by adding energy for instance).

Are critical and failure events ? or state variations ? => state variations are better because they do not induce  a nec cyccle, it is a **fact** that after that card is played there is x% of that state, y% of this state, etc ... and it allows us to immédiately asked what card woould now be allowed.