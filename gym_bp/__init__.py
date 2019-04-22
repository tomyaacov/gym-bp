from gym.envs.registration import register

register(
    id='BP-v0',
    entry_point='gym_bp.envs:BPEnv',
)
