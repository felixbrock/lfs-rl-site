@kpis
3 :: environments in the suite
104 :: machine-verified short-horizon instances
58% :: held-out-variant attempts solved after RL, from 0% base
3&hairsp;/&hairsp;3 :: flagships reproduce the incident, no signal present
108 :: failures from real operation classified into 19 modes

**Abstract.** Agents increasingly operate real systems without supervision, and the incidents they cause there are rarely capability failures. Every flagship we measured can perform the repair, what fails is the step before, checking the current state of the world instead of acting on a remembered one, the same step behind 48 of the first 108 failures logged in real operation. This suite makes that step, route to the deciding evidence first, measurable and trainable, with a bigger haystack around the evidence at each of its three levels. Three flagships (Claude Fable 5, gpt-5.6-sol, Hermes 4 405B) reproduce a real recorded incident in most or all episodes when no signal prompts them to look and in 0 of 30 episodes when one does, and unsupervised operation is exactly the setting where nobody provides the signal. A 3-billion-parameter model trained to look first fully solves 58% of its attempts on unseen variants of its repair problems and none on a library absent from training, and the first two prevention-training updates on the incident tasks ran on 2026-08-17.

| Horizon | Where the evidence hides | Example |
|---|---|---|
| <b>1</b>&ensp;small | one named package and its build environment | kmod fails to link, the evidence is one mispointed symlink in zlib |
| <b>2</b>&ensp;medium | anywhere across 80 packages | the build fails at package&nbsp;9, the cause lies at package&nbsp;4 |
| <b>3</b>&ensp;large | in the situation itself | the system is no longer the build environment the agent remembers, it is live production |

Origin of the tasks. We ran Claude Fable 5 from July to September 2026 as the administrator of a real Linux system, and its failures from 2026-08-10 on are recorded in a log that also records failures of three other Claude models ([Section&nbsp;6](#failure-log)). Given a specific problem to repair, it almost always repaired it, and what it missed was **noticing that something was wrong at all**. The incident tasks of [Section&nbsp;4](#ops-derived-procedural-tasks) replay failures recorded on this system, several families of repair problems generalize failure mechanisms from its operating records or from the build of this suite, and the remaining problems were designed by hand. Every task is graded mechanically, mostly by whether a real program executed inside the repaired system produces the correct output, never by a judge model or an answer string. The task texts, fixtures, and graders are deliberately unpublished, a public copy would enter future models' training data and turn this evaluation into a memory test.

**The central measured result.** We replayed the model's worst real incident as a controlled experiment, twenty-five fresh episodes on one exactly reproducible fault. Two signals could alert the model, a statement that the situation had changed, or a task that points at the hazard. With either signal present it never failed. With both absent, the hazard buried in a routine queue, it reproduced its own recorded incident (Figure&nbsp;1).

{{figure-1}}

The gap is therefore neither knowledge nor skill. The safety information was on disk in every episode, and when the task pointed at the hazard the model applied it correctly, even against its own minutes-old "this worked before" success (5 of 5). It failed only when nothing prompted it to read the guidance, and in one such episode it read the pointer to the guidance and still installed the old way. This look-before-acting habit is the routing skill from the opening table, and the suite exists to measure and train it, because the more autonomous the deployment, the less often anything else provides the prompt.

{{listing-1}}

## 1 One skill, three horizons {#one-skill-three-horizons}

The three environments are the three rows of the opening table, and the routing skill was found in the data, not chosen in advance. Small horizon, a trained model only generalized after its training examples opened by checking the deciding evidence, most when every example opened with the same three checks (held-out attempts that ran checks for more than one fault family, 4 of 24 to 22 of 24). Medium horizon, the frontier model found one inconsistent file among eighty packages, the cause of a failure five packages downstream. Large horizon, Figure&nbsp;1, the frontier fails exactly when nothing prompts it to look. Training climbs small to large, and incidents that never become training material are kept aside as the final exam.

All three share one agent-facing contract, a shell and one command per turn, and the same functional grading, but they run on different substrates and are trained or evaluated separately.

| Environment | The agent's task | Status |
|---|---|---|
| <b>1</b>&ensp;Short-horizon repair | repair a named broken package | trained and evaluated (Fig.&nbsp;2) |
| <b>2</b>&ensp;Long-horizon localization | find the cause, told nothing | built and machine-verified |
| <b>3</b>&ensp;Ops-derived procedural | replay of a real incident | built, measured on three flagships (Fig.&nbsp;1, 4, 6), first training updates (Fig.&nbsp;5) |

@kick Environment 1 of 3
## 2 Short-horizon repair {#short-horizon-repair}
@status Trained and evaluated. The only environment with a measured training gain.

Training is effective at this level. The agent is told which package fails and must repair the cause, 119 instances across five libraries, 104 of them machine-verified by 2026-08-18 and 15 awaiting a virtual machine, including a group where the error message blames the wrong component by design. The five library verifiers perform a real compression or parse, so a stub library that fakes only the version string cannot pass, and one such stub we built was rejected in testing. A small model (Qwen2.5-3B) starts at 0% and after training solves **58% of its attempts on six problems it never saw**, 14 of 24, each a new variant of a trained fault type (Figure&nbsp;2). On three problems from a library absent from training it solves 0 of 12 attempts after supervised training and after RL, the base model solved none of 6 earlier attempts on that library, and no teaching example shows its build recipe. Claude Fable 5 solved six representative problems of this level in 7 to 18 commands, one attempt each, so this level trains and evaluates open models rather than challenging the frontier.

Additional example repairs alone produced no generalization, the model reproduced what it was shown. An earlier run trained on plain replayed repairs solved 9 of its 18 trained problems (0 of 18 at base, exact McNemar p&nbsp;=&nbsp;0.004) and 0 of 11 problems it never saw, one attempt each. Transfer first appeared once every teaching example opened with the check that reveals the fault, 3 of 16 held-out attempts after supervised training and 5 of 16 after RL, one fault family. It grew once every example opened with the same three read-only checks, so an example no longer revealed which check to run. Same tasks, same model, different examples, solved held-out attempts rose from 3 of 24 with family-specific opening checks to 8 of 24 after supervised training alone and to 14 of 24 after RL.

{{figure-2}}

@kick Environment 2 of 3
## 3 Long-horizon localization {#long-horizon-localization}
@status Built and machine-verified. One frontier calibration episode, untrained.

We inject a fault into one package and allow the build to continue, so the visible failure surfaces later, up to fourteen packages downstream in the verified tasks. The agent is told nothing about where to look. Before a task counts, a machine check proves the injected fault causes the failure, patching where the failure surfaces does not repair it, and repairing the true cause does. Two candidates failed the proof that the injected fault causes the failure and were retired from the task set, the checker filters rather than approves. Difficulty is an adjustable parameter, the same fault type passes at distance 5 and at distance 14, with 80 packages in the build sequence available for expansion.

{{figure-3}}

Claude Fable 5 has attempted one instance, at distance 5, and solved it in 24 of the 40 permitted commands through genuine diagnosis, rebuilding the suspect library from clean source and comparing it byte by byte against the installed copy. Every episode here still opens by announcing that something is broken, which is what the model was always good at. The unannounced variants are the same unmeasured settings as in Figure&nbsp;1 and remain on the roadmap.

@kick Environment 3 of 3
## 4 Ops-derived procedural tasks {#ops-derived-procedural-tasks}
@status Built and machine-verified. Thirty-one Claude Fable 5 episodes scored, two RL training updates run and measured on 2026-08-17.

This level is built from the real incident, nothing in it is artificially broken, the hazard is an old procedure meeting a changed world. In the **live-install** family, the agent holds an upgrade script written for a system under construction and must apply a security update to a system that is now live. Executed as written, the script replaces a library the running shell itself depends on, and partway through the replacement the system loses the ability to start a new process. The safe procedure, read the written guidance for this update, stage the new files beside the live ones, replace each with one atomic rename, in the correct order. In the **false-failure** family the trap is inverted, an upgrade succeeds and then reports failure because its verification step has a timing bug, and the agent must prove the system healthy instead of "fixing" it.

The transcripts of the first no-signal run in Figure&nbsp;4 (3 of 5 reproduced) state why its failures occur. No failing agent read that guidance before acting, and both agents that held read it first. Each failure is a failure to route to the evidence, the skill in the opening table. Two clarifications, the reward scores prevention and recovery separately (the real incident was also recovered, recovery alone must not look like success), and one extra episode ended in a refusal over doubts about a file's origin, a reasonable outcome our grading cannot yet score, kept as an open design item.

{{figure-4}}

**Two training updates ran on this environment on 2026-08-17 (Figure&nbsp;5).** After every command the harness checks, invisibly to the agent, whether the system can still start a process, and an episode that ever fails the check scores zero even if repaired afterward. The full task is beyond a 3-billion-parameter model, every attempt fails the same way, and uniform outcomes carry no learning signal. A reduced form, in which preparation is complete and only the install decision remains, splits the outcomes, and the small model performs the same unsafe install the frontier performed. Each update pushed the policy away from the episode that broke the system, and the head-to-head afterward, 2 broken systems in 8 episodes instead of 3, is a direction and not a learning claim, because two earlier evaluations of the same warm-start policy broke the system in 1 and 2 of 8 episodes.

{{figure-5}}

@kick Cross-model
## 5 Other flagships on the same incident {#other-flagships}
@status Measured. Twenty-one episodes across two hosted flagships, August 2026.

The missing-signal failure is not specific to one vendor. **Hermes 4 405B** (Nous Research) and **gpt-5.6-sol** (OpenAI) ran the live-install episode through a hosted API on the two corner arms of Figure&nbsp;1, strongest signal and no signal, keeping the two-phase design, a routine rebuild first, then the hazard later in the same episode. With the signal, 10 of 10 held across both models. Without it, Hermes reproduced the incident in 4 of 6 and sol in 5 of 5. The Figure&nbsp;1 contrast holds for all three models measured.

{{figure-6}}

The models differ in what happens after the window opens. Hermes recovered in one of its four reproduced episodes, after five commands in which the system could not start a process, and the other three ended with the system still unable to start one. Sol recovered every time, detected the fault within one or two commands, repaired the library from outside, and passed all five episodes, the exact shape of the recorded incident, damage then competent repair, and on a live system a two-command outage is still an outage. The transcripts show the decisive moment, sol read the update guidance and concluded, verbatim, "The guidance explicitly permits plain installation inside this non-running chroot". That had stopped being true one phase earlier, and the files saying so sat unread on disk, a stale fact carried forward instead of rechecked, the routing failure this suite trains.

Hermes exhibits a second failure mode, verification by narration. It writes several commands and their imagined results in one turn, the protocol executes one command per turn, so most of its plan never executes and the model does not notice. A mechanical check catches the consequence, the opening task's library rebuild really happened in 10 of 10 sol episodes but in only 2 of 11 Hermes episodes (ten checked mechanically, one from its transcript), and in four episodes Hermes declared the whole task complete after 2 to 5 commands, having changed nothing.

The two Anthropic models could not be measured, Anthropic's API-side safety filter blocks the episodes. Fable is blocked at the task text, every reply arrives empty. Opus 5 begins working and is interrupted mid-episode in 7 of 10 episodes, where the filter blocks the accumulated transcript although the task text alone passes, and we did not alter prompts to route around the filter. The 3 unblocked Opus episodes all ended as full safe passes, one of them in the unsignaled queue, and 3 episodes support no rate. The filter is part of the scaffold, and for Anthropic's models it is the binding constraint on this task family.

Two caveats scope these numbers. The Figure&nbsp;1 episodes ran inside Claude's own agent product, the new models ran through a minimal text protocol, so rates compare within a model, not across models. Each arm holds 5 or 6 episodes. Pooled across both models the no-signal episodes (9 of 11 reproduced) span 48 to 98% at exact 95% confidence, the signal episodes (0 of 10) span 0 to 31%, and Hermes alone (22 to 96%) is too wide to support a claim on its own. The 21 episodes cost $4.45, the blocked Opus attempt roughly $11 and the blocked Fable attempt about $0.02.

@kick Task source
## 6 Failures recorded in real operation {#failure-log}
@status Classified. The first 108 logged failures in 19 failure modes, 2026-08-10 to 2026-09-28.

The largest group of failures recorded in real operation is the routing failure this suite trains, 48 of the first 108 (Figure&nbsp;7). The agent that operates the real system writes one log entry per failure it makes there, with the root cause and the simple check that would have caught it, and a near-miss, a failure caught in review before it caused harm, receives an entry too. The entries name four Claude models as the model that made the failure, Fable&nbsp;5, Opus&nbsp;5, Fable&nbsp;5.1 and Opus&nbsp;5.5, and entries for failures before 2026-08-21, when the log started, were written afterward from the operating records, commits, the incident file, issues and the journal. Each entry was assigned to exactly one of 19 failure modes, and the modes fall into four groups. Two modes have task families in [Section&nbsp;4](#ops-derived-procedural-tasks), the live-install incident and the false-failure verifier.

{{figure-7}}

Recording a failure did not prevent its recurrence. A process search that matched the shell running the search itself recurred in six later entries. Placing a file with no recorded checksum in a directory where every file must match one recurred four times. Each recurrence occurred with the first entry already in the log, and the operator's start-of-session procedure does not read the log. As in Figure&nbsp;1, the information that would have prevented the failure was on disk, and nothing prompted a read.

These counts describe one log and are not rates. One annotator, the Claude Opus&nbsp;5.5 operator, assigned the modes from each entry's recorded root cause. No second annotator checked the assignment, so an entry near the boundary between two modes reflects one judgment. The four models operated in different periods on different work, so the log does not compare models.

## 7 Properties shared across the suite {#properties}
@spec
Format :: the short-horizon level plugs into standard RL tooling (packaged as a `verifiers` environment) and has been run end to end against a live model
Determinism :: the same seed reproduces the same fault and the same verifier
Cost :: what is shared is the substrate, every episode runs in the same rootless sandbox and restarts from a cached snapshot, except the 15 level 1 instances that need a virtual machine. Cost then scales with horizon. A level 1 episode that replays the known correct repair, with no model in the loop, measures about <b>1.6 seconds</b> and 200 MB, and the training run behind Figure&nbsp;2 cost about <b>$2.60</b> of GPU time including its evaluations. Level 3 training rounds of eight episodes took about 30 minutes each, and its two training sessions on 2026-08-17 cost <b>$1.64</b> and <b>$1.95</b>. Level 2 episodes are dominated by the commands the agent runs, and level 2 is untrained
Isolation :: allow-list filesystem and private loopback-only network, verified by writing a marker from inside into every host directory that was reachable before the allow-list, and confirming none arrived
Scaling :: 13 fault types are generated from each package definition, so adding a library means a package definition, one checking script and entries in four per-package tables, and those 13 fault types then apply to it unchanged

## 8 Design basis {#design-basis}

One published design is applied in the current system. [RLVE](https://arxiv.org/abs/2511.07317) showed a learner needs tasks it sometimes solves and sometimes fails, and that principle produced the Figure&nbsp;5 result, the full incident task measured all-fail, so a reduced form was built until outcomes split. The substrate already restarts every episode from a cached snapshot and can fork the build at any package (verified). The two designs that would exploit this, [BPO](https://arxiv.org/abs/2607.14171)-style forked rollouts and [TRACE](https://arxiv.org/abs/2607.13988)-style per-step credit, are unimplemented roadmap items.

## 9 Next measurements {#next-measurements}

The roadmap follows directly from what the current numbers can and cannot yet say.

@spec
Wider arms :: rerun the Figure&nbsp;1 arms at 20 or more episodes each, so every cell reports a rate with a confidence interval instead of a count, and fill in the two off-corner arms for the hosted models of [Section&nbsp;5](#other-flagships)
A second incident :: rebuild the 2x2 on a different recorded incident, testing whether the cue sensitivity generalizes beyond this fixture, the second-model half is measured in [Section&nbsp;5](#other-flagships)
Isolating self-distrust :: an arm where the only safety evidence is the model's own contradicted history, separating trust in stale experience from the routing of external information
Training rigor :: repeat the Qwen run several times with different random seeds and several attempts per problem, reporting ranges in the style of [Agarwal et al., 2021](https://arxiv.org/abs/2108.13264), so seed variance is separated from the RL gain
Prevention training :: continue the live-install GRPO program past its first two verified updates, more rounds and 20-plus-episode evals, until the brick-rate delta carries a confidence interval rather than a direction
An external anchor :: select one external terminal-task benchmark on which the base 3B scores nonzero-but-low (a band test before any claim rides on it), run it at every training level, and pair it with a negative control on which the trained model must not improve
Exam integrity :: training and exam material stay disjoint by incident, so mining new incidents from continuing operation ([Section&nbsp;6](#failure-log)) is a standing prerequisite, the live-install incident carries training forms, and only incidents free of them count as the exam
Forked rollouts (BPO) :: implement the training loop that forks an episode at a decision point and compares the siblings, the fork-native substrate is built and verified, the algorithm is not
Per-step credit (TRACE) :: assign reward to individual commands from the per-step probe timeline instead of whole episodes, the adaptation is designed and the probe already records the needed signals
Long-horizon settings :: score the distance-14 instance and the episode variants that never announce a fault, the settings [Section&nbsp;3](#long-horizon-localization) leaves unmeasured
