import argparse

def get_defaults():
  
  parser = argparse.ArgumentParser()
  # ========================================================================
  # Sim
  # ========================================================================
  parser.add_argument('--render', default=False, action="store_true")
  parser.add_argument('--urdf', default=False, action="store_true")
  parser.add_argument('--cur', default=False, action="store_true")
  parser.add_argument('--hpc', default=False, action="store_true")
  parser.add_argument('--test', default=False, action="store_true")
  parser.add_argument('--perception', default=False, action="store_true")
  parser.add_argument('--apply_disturbances', default=False, action="store_true")
  parser.add_argument('--record_sim', default=True, action="store_false")
  parser.add_argument('--best', default=False, action="store_true")
  parser.add_argument('--emitter', default="")
  parser.add_argument('--folder', default="")
  parser.add_argument('--reward', default="")
  
  parser.add_argument('--exp', default="test")
  parser.add_argument('--sleep', type=float, default=0.01)


  # ========================================================================
  # Running
  # ========================================================================
  parser.add_argument('--stacked', type=int, default=1)
  parser.add_argument('--env', default="")

  
  # ========================================================================
  # Training
  # ========================================================================
  parser.add_argument('--seed', type=int, default=42)
  parser.add_argument('--save_freq', type=int, default=10)
  parser.add_argument('--steps', type=int, default=2048)
  parser.add_argument('--epochs', type=int, default=8000)
  parser.add_argument('--cpu', type=int, default=1)
  parser.add_argument('--episodes', type=int, default=100)

  # ========================================================================
  # Terrain
  # ========================================================================
  parser.add_argument('--terrain_first', default=False, action="store_true")
  parser.add_argument('--add_terrain', default=False, action="store_true")
  parser.add_argument('--initial_terrain_difficulty', type=float, default=0.01)
  parser.add_argument('--final_terrain_difficulty', type=float, default=0.5)
  parser.add_argument('--difficulty', type=int, default=1)

  # knowns, unknowns = parser.parse_known_args()
  args = parser.parse_args()
  return args
