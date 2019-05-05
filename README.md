##gym-bp
To install the environment, just go to the gym-bp folder and run the command -
<br>
<b>
pip install -e .</b>
<br>
This will install the gym environment. Now, we can use our gym environment with the following -
<br>
<b>
import gym<br>
import gym_bp<br>
env = gym.make('BP-v0')<br>
env.source_name = "rumba_discrete"<br>