### Hi, I'm Janat.

I'm an AI-engineering student. I like building things you can open and poke at, then measuring them honestly: held-out sets, inter-patient splits, and the errors written down next to the wins. Two of the projects below come with a written paper.

---

#### Models, and how well they actually do

<table>
<tr>
<td width="50%" valign="top">

<b><a href="https://github.com/Janat-Yasser/heart_simulator">CardioSim</a></b>: a bedside ECG monitor simulator. Every beat is labelled by a 9,000-parameter CNN I trained on MIT-BIH, using an inter-patient split so the test patients were never seen in training. It catches ventricular beats well (91% sensitivity, 90% PPV); the paper says plainly where it doesn't work.
<br><br>
<sub>Python · PyQt5 · NumPy · paper</sub>

</td>
<td width="50%" valign="top">

<img src="https://raw.githubusercontent.com/Janat-Yasser/heart_simulator/main/docs/monitor.gif" alt="CardioSim switching from sinus rhythm to ventricular tachycardia" width="100%">

</td>
</tr>
<tr>
<td width="50%" valign="top">

<img src="https://raw.githubusercontent.com/Janat-Yasser/rag-faithfulness-detector/main/docs/factcheck.gif" alt="An answer being fact-checked claim by claim against its sources" width="100%">

</td>
<td width="50%" valign="top">

<b><a href="https://github.com/Janat-Yasser/rag-faithfulness-detector">RAG Faithfulness Detector</a></b>: does an AI answer say what its sources say? It checks claim by claim, without calling a language model. It scored 86% on a held-out set where the first version scored 46%. <a href="https://janat-yasser.github.io/rag-faithfulness-detector/">Try it in your browser</a>.
<br><br>
<sub>Python · scikit-learn · paper</sub>

</td>
</tr>
</table>

#### Things you can open in a browser

| Project | What it is |
|---|---|
| **[AlgoViz](https://github.com/Janat-Yasser/algoviz)** | Sorting, pathfinding and trees, step by step, with sound and a race mode. [Live](https://janat-yasser.github.io/algoviz/) |
| **[Systems Playground](https://github.com/Janat-Yasser/sysplay)** | Cut a network cable, watch Huffman build its tree, scan a key-value store. [Live](https://janat-yasser.github.io/sysplay/) |
| **[Attendly](https://github.com/Janat-Yasser/attendly)** | Class attendance for three roles, with early warnings before a student hits the absence limit. [Live](https://janat-yasser.github.io/attendly/) |

#### Larger builds

- **[RoboForge](https://github.com/Janat-Yasser/Roboforge)**: describe a robot once and get firmware, ROS 2 packages and wiring docs, then watch it drive in a 2D simulator first. TypeScript monorepo with CI.
- **[DebateBot](https://github.com/Janat-Yasser/debatebot)**: an LLM argues the other side of a motion from a sourced evidence base, then a judge model scores the debate.
- **[HirePath](https://github.com/Janat-Yasser/hirepath)**: a job board where each application's match score comes with the matched and missing skills behind it.

#### Working on next

A medical-imaging model, trained and evaluated the same way: a public dataset, a split that can't leak, calibration, and an explanation of what the model is looking at.

---

<sub>Code in these repositories is public to read, not licensed for reuse. © 2026 Janat Yasser.</sub>
