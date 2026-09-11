import pytest

def test_workflow_node_version():
    """Regression test ensuring Node v18 statically."""
    import yaml
    with open('sample_data/ci_configs/sample_workflow.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    steps = config['jobs']['build']['steps']
    setup_node_step = next(s for s in steps if 'setup-node' in s.get('uses', ''))
    assert setup_node_step['with']['node-version'] == '18.x'