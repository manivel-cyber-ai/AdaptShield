# AdaptShield

**An adversarial self-learning firewall — Red Agent vs. Blue Agent in a closed reinforcement-learning loop.**

AdaptShield explores whether a defensive AI (Blue Agent) can learn to detect and block network intrusions by training continuously against an attacking AI (Red Agent) that adapts its strategy in response. Instead of a static, rule-based firewall, the system evolves — each side pressures the other to improve.

---

## Motivation

Traditional firewalls and IDS/IPS systems rely on static rules or signatures, which struggle against novel or evolving attack patterns. AdaptShield is a research/portfolio project investigating a self-play approach — similar in spirit to how AlphaGo used self-play to improve — applied to network defense instead of a board game.

---

## Core Concept

- **Red Agent** — an RL-trained attacker that learns to probe, evade, and exploit the environment (e.g., port scans, brute force, injection attempts, exfiltration).
- **Blue Agent** — an RL-trained defender that learns to detect and respond (e.g., block IP, rate-limit, isolate, alert).
- **Closed loop** — both agents train simultaneously in a simulated network environment, each adapting to the other's evolving strategy.

---

## Status

🚧 **Early development.** Project scaffold in progress. See [Roadmap](#roadmap) below for current stage.

---

## Roadmap

- [ ] Define environment spec (states, actions, rewards for both agents)
- [ ] Build simulated network environment (Python + Gymnasium)
- [ ] Train Blue Agent baseline on labeled dataset (CICIDS2017 / NSL-KDD / UNSW-NB15)
- [ ] Add Red Agent as scripted (non-learning) attacker; validate Blue detection
- [ ] Make Red Agent learn (RL) against static Blue Agent
- [ ] Close the loop — simultaneous adversarial training
- [ ] Log training curves, win rates, attack diversity
- [ ] Write up results / paper

---

## Tech Stack (planned)

| Component | Tool |
|---|---|
| RL framework | Gymnasium, Stable-Baselines3 (or custom PPO/DQN) |
| Datasets | CICIDS2017, NSL-KDD, UNSW-NB15 |
| Language | Python |
| Firewall mapping | iptables/nftables (Linux) |
| Compute | Local (CPU prototyping) → Kaggle/Colab (GPU training) |

---

## Repo Structure

```
adaptshield/
├── docs/               # Paper presentation slides, diagrams, writeups
├── env/                # Simulated network environment (Gymnasium)
├── agents/
│   ├── red/            # Attacker agent
│   └── blue/           # Defender agent
├── data/                # Dataset loaders / preprocessing (raw data not committed)
├── notebooks/           # Kaggle/Colab experiment notebooks
├── logs/                 # Training run logs, metrics (gitignored large files)
├── requirements.txt
└── README.md
```

---

## Getting Started

```bash
git clone https://github.com/manivel-cyber-ai/adaptshield.git
cd adaptshield
pip install -r requirements.txt
```

*(Setup instructions will be expanded as the environment and agents are built.)*

---

## Contributors

- [Harish Karthikeyan C](https://github.com/Harish-aiml)
- [Manivel R](https://github.com/manivel-cyber-ai)

---

## Documentation

Project presentation slides are available in [`docs/`](./docs).

---

## License

*(Add a license — MIT is a common choice for research/portfolio projects.)*

