from gymnasium.envs.registration import register

register(
    id="carRace/NamCTrack-v0",
    entry_point="carRace.envs:NamCTrackEnv",
    max_episode_steps=1e+10
)