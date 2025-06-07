# tests/test_demo.py
import sys
import pathlib
import pytest


root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from scripts.run_demo import chinese_postman_cost, load_graph

def test_demo_cost_positive(tmp_path):
   
    csv_file = tmp_path / "test_edges.csv"
    csv_file.write_text("u,v,length\n0,1,100\n1,0,100")
    G = load_graph(str(csv_file))
    cost = chinese_postman_cost(G)
    assert cost > 0, "Le coût doit être strictement supérieur à 0"
