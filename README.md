# Revity

**A vision for capable local AI with a smaller environmental footprint.**

Revity aims to make useful AI available on your own hardware, with efficiency and responsible resource use at the heart of its design. The goal is simple: build an assistant that helps people while being thoughtful about the resources it takes to run.

> **Project status:** Dataset development stage. The repository includes reproducible synthetic starter data, an evaluation scorer, and automated tests. There is no trained Revity model or runnable AI assistant yet. A Qwen-based Revity 1.0 is a goal, not an available model release.

## Starter datasets

Generate **12,000 examples across six task families** using Python 3.10+:

```sh
python scripts/build_datasets.py --output data/generated
python -m unittest discover -s tests -v
```

The data covers arithmetic, linear equations, sorting, unit conversion, word counting, and Boolean logic. Training, validation, and test splits have no identical prompts, but share templates. See the [dataset documentation](data/README.md) for provenance, limitations, and evaluation instructions. These are narrow synthetic tasks, not a broad knowledge corpus or proof of model reasoning ability.

## The vision

- **Run locally:** Work toward an AI assistant that runs on your own device.
- **Be useful:** Focus on practical assistance and build capabilities step by step.
- **Use resources efficiently:** Consider hardware requirements, energy use, and cooling needs alongside model quality.
- **Measure the impact:** Support environmental claims with clear measurements as the project develops.

These are project goals, not features available today.

## What does “no water for cooling” mean?

Revity's original ambition is to run local AI without water-based cooling. Whether that is possible depends on the hardware and cooling system used; software alone cannot guarantee it.

Running locally also does not mean having zero environmental impact. Electricity generation and hardware manufacturing can use water and other resources. As Revity develops, the aim is to describe those tradeoffs honestly and distinguish direct cooling needs from the wider footprint.

## Planned next steps

- [ ] Define the assistant's first use cases and target hardware.
- [ ] Evaluate models and local inference tools for capability and efficiency.
- [ ] Build a minimal working prototype.
- [ ] Document installation, hardware requirements, and local usage.
- [ ] Measure performance and resource use under documented conditions.

This is an initial direction, and priorities may change as the project learns what works.

## Getting started

There is no AI assistant to run yet. You can follow development on [GitHub](https://github.com/Cocopuff2223/Revity) or clone the repository to generate the starter datasets:

```sh
git clone https://github.com/Cocopuff2223/Revity.git
cd Revity
```

The dataset tools use only Python's standard library. Assistant setup instructions will be added when a working prototype is available.

## Contributing

Ideas, research, and constructive feedback are welcome. Useful starting points include:

- Suggesting practical tasks for the first prototype.
- Comparing local models and their hardware requirements.
- Proposing ways to measure energy use and cooling needs.
- Improving documentation and making the goals more precise.

Use [GitHub Issues](https://github.com/Cocopuff2223/Revity/issues) to share an idea or discuss a substantial change before starting work. For documentation improvements, open a pull request with a brief explanation of your changes.

## License

Generated dataset contents are dedicated under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). No source-code license has been added yet. The dataset dedication does not grant rights to any external model; a base model's license must be reviewed separately before redistribution.
