# Project Goal
The goal of this project is to create a randomized, yet robust schedule for "random coffee" pairings. The pairings should follow the logic:

1. Each participant should meet with ALL other participants before meeting again with the same participant.

e.g., - `A`, `B`, `C`, and `D` are participants. `A` must meet with `B`, `C`, and `D` before being allowed to meet with B for a second time. The order which `A` meets with `B`, `C`, and `D` does not matter, so long as `A` meets with each before having a repeat meeting with any one individual.

2. Participant pairings should not duplicate week-to-week.

e.g., `A`, `B`, `C`, and `D` are participants. After meeting with `B`, `C`, and `D` (in that order), `A` can meet with `B`, `C`, or  `D`, given rule (1). However, rule (2) requires `A` to meet with either `B` or `C` before meeting again with `D` to ensure that meetings are not duplicated back-to-back. Stated another way - `A`'s schedule is required to be:

- Week 1: `B`
- Week 2: `C`
- Week 3: `D`
- Week 4: `B`/`C`
- Week 5: `B`/`C`/`D`
- Week 6: `B`/`C`/`D`
- ...

to ensure that weeks 3 and 4 do not have `A` and `D` meeting in both weeks.

## Note
The script is non-deterministic and will likely generate a different resulting schedule each time you run it.
