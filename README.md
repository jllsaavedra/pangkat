<div align="justify">

PANG-KAT is a dedicated, hybrid rule and dictionary-based tokenizer for the Tagalog language that also incorporates the recognition of Tagalog named entities (NEs), multi-word expressions (MWEs), and Taglish tokenization, to develop a general tokenizer for real-world Tagalog language processing applications. 

It is designed to address the lack of language-specific NLP tools for Tagalog, despite it being one of the most widely spoken languages in the Philippines, with the hope of serving as one of the foundational tools needed to promote its further NLP exploration. 

In this study, PANG-KAT was developed as a hybrid rule and dictionary-based tokenizer due to the lack of pre-annotated, publicly available resources for a machine-learning approach. It was designed to be implemented as a Python module, which can be imported into more advanced Tagalog NLP applications as its tokenizer. To facilitate the evaluation of its performance, a GUI was developed to provide a visual representation of its tokenization results. The results of PANG-KAT are stored in independent arrays of tokens and their corresponding labels for both short and longer unit tokenization, which it returns as a module or can be downloaded in either JSON or CSV format using its GUI.

<h3> DIRECTORIES AND FILES </h3>

<ol>
  <li>Binary - Contains "dependency.explain" file that lists the dependencies needed for PANG-KAT.</li>
  <li>Data - Contains folders of each respective dataset used for evaluating PANG-KAT’s performance for both unit testing and external validation.</li>
  <li>Document - Contains PANG-KAT's journal articles (in IEEE and IURS format), manuscript, IURS poster, manual, and presentation materials.</li>
  <li>
    Source
    <ol>
      <li>Document - Contains the doc files of PANG-KAT's manuscript and manual, as well as the image assets, LaTeX, and BibTex files used to create PANG-KAT's journal.</li>
      <li>Program - Contains the codebase for PANG-KAT as a module and with a GUI. To use PANG-KAT as a module, download the “module” folder and import PANG-KAT in your Tagalog NLP application as its tokenizer. To use PANG-KAT with its GUI, download the “with GUI” folder and run pangkat.exe.</li>
    </ol>
  </li>
  <li>Videos - Contains the video demonstration on how to use PANG-KAT both as a module and with a GUI.</li>
  <li>The "Saavedra, Justin Louis L.txt" file contains the author’s information. </li>
</ol>

</div>
