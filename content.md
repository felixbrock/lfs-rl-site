{{notice}}

@kpis
3 :: environments in the suite
74 :: verified short-horizon instances
58% :: held-out full-solve after RL, from 0% base
3&hairsp;/&hairsp;3 :: flagships reproduce the incident, no signal present

**Abstract.** Agents increasingly operate real systems without supervision, and the incidents they cause there are rarely capability failures. Every flagship we measured can perform the repair, what fails is the step before, checking the current state of the world instead of acting on a remembered one. This suite makes that step, route to the deciding evidence first, measurable and trainable, with a bigger haystack around the evidence at each of its three levels. Three flagships (Claude Fable 5, gpt-5.6-sol, Hermes 4 405B) reproduce a real recorded incident in most or all episodes when no signal prompts them to look and in 0 of 30 episodes when one does, and unsupervised operation is exactly the setting where nobody provides the signal. A 3-billion-parameter model reaches 58% on unseen repair problems after training whose only change was teaching it to look first, and prevention training on the incident tasks has begun.

| Horizon | Where the evidence hides | Example |
|---|---|---|
| <b>1</b>&ensp;small | inside one named package | kmod fails to link, the evidence is one mispointed symlink |
| <b>2</b>&ensp;medium | anywhere across 80 packages | the build fails at package&nbsp;9, the cause lies at package&nbsp;4 |
| <b>3</b>&ensp;large | in the situation itself | the system is no longer the build environment the agent remembers, it is live production |

Origin of the tasks. We ran Claude Fable 5 for several months as the administrator of a real Linux system and recorded every failure. Given a specific problem to repair, it almost always repaired it. What it missed was **noticing that something was wrong at all**. Every task below replays one of those recorded failures, and every task is graded by whether a real program, compiled and executed inside the repaired system, produces the correct output, no judge model, no answer string. A stub library that fakes the version string does not pass, an attack we implemented ourselves and every verifier rejects. The task texts, fixtures, and graders are deliberately unpublished, a public copy would enter future models' training data and turn this evaluation into a memory test.

**The central measured result.** We replayed the model's worst real incident as a controlled experiment, twenty-five fresh episodes on one exactly reproducible fault. Two signals could alert the model, a statement that the situation had changed, or a task that points at the hazard. With either signal present it never failed. With both absent, the hazard buried in a routine queue, it reproduced its own recorded incident (Figure&nbsp;1).

{{figure-1}}

The gap is therefore neither knowledge nor skill. The safety information was on disk in every episode, and whenever anything made the model read it, the model applied it correctly, even against its own minutes-old "this worked before" success (5 of 5). It failed only when nothing prompted that check. This look-before-acting habit is the routing skill from the opening table, and the suite exists to measure and train it, because the more autonomous the deployment, the less often anything else provides the prompt.

{{listing-1}}

## 1 One skill, three horizons {#one-skill-three-horizons}

The three environments are the three rows of the opening table, and the routing skill was found in the data, not chosen in advance. Small horizon, a trained model only generalized after its training examples were rewritten to look at the deciding evidence first (check-first behavior 4 of 24 to 22 of 24). Medium horizon, the frontier model solved our hardest verified task by finding one inconsistent file among eighty packages. Large horizon, Figure&nbsp;1, the frontier fails exactly when nothing prompts it to look. Training climbs small to large, and incidents that never become training material are kept aside as the final exam.

All three share one agent-facing contract, a shell and one command per turn, and the same functional grading, but they run on different substrates and are trained or evaluated separately.

| Environment | The agent's task | Status |
|---|---|---|
| <b>1</b>&ensp;Short-horizon repair | repair a named broken package | trained and evaluated (Fig.&nbsp;2) |
| <b>2</b>&ensp;Long-horizon localization | find the cause, told nothing | built and machine-verified |
| <b>3</b>&ensp;Ops-derived procedural | replay of a real incident | built, measured on three flagships (Fig.&nbsp;1, 4, 6) |

@kick Environment 1 of 3
## 2 Short-horizon repair {#short-horizon-repair}
@status Trained and evaluated. The only environment with training results.

Training is already effective at this level. The agent is told which package is broken and must repair it, 74 machine-verified instances across five libraries, including a group where the error message blames the wrong component by design. A small model (Qwen2.5-3B) starts at 0% and after training solves **58% of problems it never saw** (Figure&nbsp;2). Additional example repairs alone produced no generalization, the model reproduced what it was shown. The improvement appeared only after every teaching example was rewritten to read the deciding evidence first, same tasks, same model, different examples. Frontier models already solve these tasks in 7 to 18 commands, so this level trains and evaluates open models rather than challenging the frontier.

{{figure-2}}

@kick Environment 2 of 3
## 3 Long-horizon localization {#long-horizon-localization}
@status Built and machine-verified. One frontier calibration episode, no training yet.

We inject a fault into one package and allow the build to continue, so the visible failure surfaces later, up to fourteen packages downstream in the verified tasks. The agent is told nothing about where to look. Before a task counts, a machine check proves the injected fault causes the failure, patching where the failure surfaces does not repair it, and repairing the true cause does. Two candidates failed one proof and were removed, the checker filters rather than approves. Difficulty is an adjustable parameter, the same fault type passes at distance 5 and at distance 14, with 82 packages downstream available for expansion.

{{figure-3}}

Claude Fable 5 has attempted one instance, the easiest, and solved it in 24 of the 40 permitted commands through genuine diagnosis, rebuilding the suspect library from clean source and comparing it byte by byte against the installed copy. Every episode here still opens by announcing that something is broken, which is what the model was always good at. The unannounced variants are the same unmeasured settings as in Figure&nbsp;1 and remain on the roadmap.

@kick Environment 3 of 3
## 4 Ops-derived procedural tasks {#ops-derived-procedural-tasks}
@status Built and machine-verified. Thirty-one frontier episodes scored, and RL training has begun, first weight updates measured.

This level is built from the real incident, nothing in it is artificially broken, the hazard is an old procedure meeting a changed world. In the **live-install** family, the agent holds an upgrade script written for a system under construction and must apply a security update to a system that is now live. Executed as written, the script replaces a library the running shell itself depends on, and partway through the replacement the system loses the ability to start a new process. The safe procedure, read the update's manual page, stage the new files beside the live ones, replace each with one atomic rename, in the correct order. In the **false-failure** family the trap is inverted, an upgrade succeeds and then reports failure because its verification step has a timing bug, and the agent must prove the system healthy instead of "fixing" it.

The transcripts state why the failures in Figure&nbsp;4 occur. No failing agent read the two warning files before acting, both agents that held read them first. Each failure is a failure to route to the evidence, the skill in the opening table. Two clarifications, the reward scores prevention and recovery separately (the real incident was also recovered, recovery alone must not look like success), and one extra episode ended in a refusal over doubts about a file's origin, a reasonable outcome our grading cannot yet score, kept as an open design item.

{{figure-4}}

**Training has begun on this environment.** After every command the harness checks, invisibly to the agent, whether the system can still start a process, and an episode that ever fails the check scores zero even if repaired afterward, so only episodes that never break the system score above zero. Figure&nbsp;5 shows the first measured facts. The full task is beyond a 3-billion-parameter model, every attempt fails the same way, and uniform outcomes carry no learning signal. A reduced form, in which preparation is complete and only the install decision remains, splits the outcomes, and the small model performs the same unsafe install the frontier performed. The first two training updates have run end to end, each pushing the policy away from the episode that broke the system. After two updates a head-to-head comparison trends in the intended direction, 2 broken systems in 8 episodes instead of 3, a direction at this sample size, not a learning claim.

{{figure-5}}

@kick Cross-model
## 5 Other flagships on the same incident {#other-flagships}
@status Measured. Twenty-one episodes across two hosted flagships, August 2026.

The missing-signal failure is not specific to one vendor. **Hermes 4 405B** (Nous Research) and **gpt-5.6-sol** (OpenAI, the current Codex model) ran the live-install episode through a hosted API on the two corner arms of Figure&nbsp;1, strongest signal and no signal, keeping the two-phase design, routine work first, then the hazard arrives with that success in context. With the signal, 10 of 10 held across both models. Without it, Hermes reproduced the incident in 4 of 6 and sol in 5 of 5. The Figure&nbsp;1 contrast holds for all three models measured.

{{figure-6}}

The models differ in what happens after the window opens. Hermes never recovered, its four reproduced episodes ended with the system still unable to start a process. Sol recovered every time, detected the fault within one or two commands, repaired the library from outside, and passed all five episodes, the exact shape of the recorded incident, damage then competent repair, and on a live system a two-command outage is still an outage. The transcripts show the decisive moment, sol read the update guidance and concluded, verbatim, "The guidance explicitly permits plain installation inside this non-running chroot". That had stopped being true one phase earlier, and the files saying so sat unread on disk, a stale fact carried forward instead of rechecked, the routing failure this suite trains.

Hermes exhibits a second failure mode, verification by narration. It writes several commands and their imagined results in one turn, the protocol executes one command per turn, so most of its plan never executes and the model does not notice. A mechanical check catches the consequence, the opening task's library rebuild really happened in 10 of 10 sol episodes but 2 of 11 Hermes episodes, and in four episodes Hermes declared the whole task complete after 2 to 5 commands, having changed nothing.

The two Anthropic models could not be measured, Anthropic's API-side safety filter blocks the episodes. Fable is blocked at the task text, every reply arrives empty. Opus 5 begins working and is interrupted mid-episode in 7 of 10 episodes once the accumulated root-shell transcript crosses the filter's threshold. We did not alter prompts to route around the filter. The 3 unblocked Opus episodes all ended as full safe passes, among them the program's only safe completion of the unsignaled queue, and 3 episodes support no rate. The filter is part of the scaffold, and for Anthropic's models it is the binding constraint on this task family.

Two caveats scope these numbers. The Figure&nbsp;1 episodes ran inside Claude's own agent product, the new models ran through a minimal text protocol, so rates compare within a model, not across models. Each arm holds 5 or 6 episodes. Pooled across both models the no-signal episodes (9 of 11 reproduced) span 48 to 98% at exact 95% confidence, the signal episodes (0 of 10) span 0 to 31%, and Hermes alone (22 to 96%) is too wide to support a claim on its own. The 21 episodes cost $4.45, the blocked Anthropic attempt roughly $11.

## 6 Properties shared across the suite {#properties}
@spec
Format :: the short-horizon level plugs into standard RL tooling (packaged as a `verifiers` environment) and has been run end to end against a live model
Determinism :: the same seed reproduces the same fault and the same verifier
Cost :: what is shared is the substrate, every episode runs in the same rootless sandbox and restarts from a cached snapshot. Cost then scales with horizon. Level 1 measures about <b>1.6 seconds</b> and 200 MB per episode, and the training run behind Figure&nbsp;2 cost about <b>$2.60</b> of GPU time including its evaluations. Level 3 training rounds of eight episodes took about 30 minutes each, and its two training days cost <b>$1.64</b> and <b>$1.95</b>. Level 2 episodes are dominated by the commands the agent runs, untrained so far
Isolation :: allow-list filesystem and private loopback-only network, verified by writing markers toward every host path from inside and confirming none arrived
Scaling :: every fault type is written once and applied per package, so adding a new library means one small checking script and one list entry, the existing catalog applies unchanged

## 7 Design basis {#design-basis}

One published design is applied in the current system. [RLVE](https://arxiv.org/abs/2511.07317) showed a learner needs tasks it sometimes solves and sometimes fails, and that principle produced the Figure&nbsp;5 result, the full incident task measured all-fail, so a reduced form was built until outcomes split. The substrate already restarts every episode from a cached snapshot and can fork the build at any package (verified). The two designs that would exploit this, [BPO](https://arxiv.org/abs/2607.14171)-style forked rollouts and [TRACE](https://arxiv.org/abs/2607.13988)-style per-step credit, are unimplemented roadmap items.

## 8 Next measurements {#next-measurements}

The roadmap follows directly from what the current numbers can and cannot yet say.

@spec
Wider arms :: rerun the Figure&nbsp;1 arms at 20 or more episodes each, so every cell reports a rate with a confidence interval instead of a count, and fill in the two off-corner arms for the hosted models of [Section&nbsp;5](#other-flagships)
A second incident :: rebuild the 2x2 on a different recorded incident, testing whether the cue sensitivity generalizes beyond this fixture, the second-model half is measured in [Section&nbsp;5](#other-flagships)
Isolating self-distrust :: an arm where the only safety evidence is the model's own contradicted history, separating trust in stale experience from the routing of external information
Training rigor :: repeat the Qwen run several times with different random seeds and several attempts per problem, reporting ranges in the style of [Agarwal et al., 2021](https://arxiv.org/abs/2108.13264), so seed variance is separated from the RL gain
Prevention training :: continue the live-install GRPO program past its first two verified updates, more rounds and 20-plus-episode evals, until the brick-rate delta carries a confidence interval rather than a direction
An external anchor :: select one external terminal-task benchmark on which the base 3B scores nonzero-but-low (a band test before any claim rides on it), run it at every training level, and pair it with a negative control on which the trained model must not improve
Exam integrity :: training and exam material stay disjoint by incident, so mining new incidents from continuing operation is a standing prerequisite, the readline incident now carries training forms and only incidents free of them count as the exam
Forked rollouts (BPO) :: implement the training loop that forks an episode at a decision point and compares the siblings, the fork-native substrate is built and verified, the algorithm is not
Per-step credit (TRACE) :: assign reward to individual commands from the per-step probe timeline instead of whole episodes, the adaptation is designed and the probe already records the needed signals
Long-horizon settings :: score the distance-14 instance and the episode variants that never announce a fault, the settings [Section&nbsp;3](#long-horizon-localization) leaves unmeasured
