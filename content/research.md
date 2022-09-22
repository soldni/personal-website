+++
title = "Research"
+++

# Research

Here is a list of current and past research thread I have been pursuing.
For a list of publications, hop over to the [publication page](/publications).

<div id='research-full'>

<div id='eff-info-sys'>

### Efficient Information Systems

Information systems are only [as good as they are fast][15].
How do we build systems that can quickly retrieve, process, and present succinct information to users?

I have looked at this problem from the perspective on question answering systems that operates at web-scale, focusing on both model ([Soldaini and Moschitti 2020][17]; [Matsubara et al 2022][18]) and data efficiency ([Han et al 2021][19]). I also collaborated on Embedding Recycling, a promising technique to reduce model computation across many tasks ([Saad-Falcon et al 2022][20]).

Currently, I am interested in efficient information systems for **scientific text**:

- How can NLP support efficient **skimming** of scientific literature?
- How does **search** on scientific literature look like? What NLP models work best for it? How can we efficiently train them?

</div>

<div id='cross-lang'>

### Cross-Language NLP and Information Processing

While there are hundreds of languages spoken in the world, most of the content on the web is [concentrated in a few languages][16].

I've looked at how to build cross-language information retrieval systems ([MacAvaney et al 2020][21]) and explored the use of generative models to combine information in different languages ([Muller et al 2021][22]).

In 2022, I am co-organizing [NeuCLIR][23], a shared task at [TREC][24] focused on cross-language information retrieval in Chinese, Farsi, and Russian.

Going forward I am interested in what other **domains** and **tasks** can benefit from a cross-lingual approach, with a particular eye towards **data-efficient** approaches.

</div>

<div id='generation'>

### Generative Models for Better Content Presentation

Generative NLP modes can be used to process the output of any information system to better suit the needs of the user.

I have worked on projects to improve presentation in question answering in both English ([Hsu et al 2021][31]), as well as other languages ([Muller et al 2021][22]). Before that, I also looked at using generative models for structured parsing of user input ([Rongali et al 2020][32]).

Going forward, I am interested in collaborating on other tasks that can use **generation** to **refine the output** of information systems, particularly in scientific settings.

</div>

<div id='oss-nlp'>

### Open-Source for NLP

I enjoy building open source tools and data for NLP and ML practitioners, such as:

- [**`smashed`**][25] is library of composable text and tensor processing functions. Compatible with [TorchData][26] and [HuggingFace Datasets][27]!
- [**`springs`**][28] is a simple library to create type-safe configuration and command-line apps that use them.
- [**`trouting`**][29] is a type-based function routing library for Python. Like `typing.overload`, but for runtime.
- [**`QuickUMLS`**][30] is a tool for fast, unsupervised biomedical concept extraction from medical text.

</div>

</div>

[15]: https://web.archive.org/web/20220922170031/https://www.nytimes.com/2012/03/01/technology/impatient-web-users-flee-slow-loading-sites.html
[16]: https://www.semanticscholar.org/paper/Tracking-Knowledge-Propagation-Across-Wikipedia-Valentim-Comarela/a3907f55ab5e5853351529db8e03e5784a93a368
[17]: https://doi.org/10.18653/v1/2020.acl-main.504
[18]: https://arxiv.org/abs/2201.05767
[19]: https://aclanthology.org/2021.eacl-main.261
[20]: https://arxiv.org/abs/2207.04993
[21]: https://doi.org/10.1007/978-3-030-45442-5_31
[22]: https://arxiv.org/abs/2110.07150
[23]: https://neuclir.github.io/
[24]: https://trec.nist.gov/
[25]: https://github.com/allenai/smashed
[26]: https://pytorch.org/data/beta/index.html
[27]: https://huggingface.co/docs/datasets/
[28]: https://springs.soldaini.net/
[29]: https://github.com/soldni/trouting
[30]: https://github.com/Georgetown-IR-Lab/QuickUMLS
[31]: http://dx.doi.org/10.18653/v1/2021.findings-acl.374
[32]: https://doi.org/10.1145/3366423.3380064
