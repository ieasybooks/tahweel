<div align="center">
  <a href="https://pypi.org/project/tahweel" target="_blank"><img src="https://img.shields.io/pypi/v/tahweel?label=PyPI%20Version&color=limegreen" /></a>
  <a href="https://pypi.org/project/tahweel" target="_blank"><img src="https://img.shields.io/pypi/pyversions/tahweel?color=limegreen" /></a>
  <a href="https://github.com/ieasybooks/tahweel/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/pypi/l/tahweel?color=limegreen" /></a>
  <a href="https://pepy.tech/project/tahweel" target="_blank"><img src="https://static.pepy.tech/badge/tahweel" /></a>

  <a href="https://github.com/ieasybooks/tahweel/actions/workflows/pre-commit.yml" target="_blank"><img src="https://github.com/ieasybooks/tahweel/actions/workflows/pre-commit.yml/badge.svg" /></a>
  <a href="https://github.com/ieasybooks/tahweel/actions/workflows/tests.yml" target="_blank"><img src="https://github.com/ieasybooks/tahweel/actions/workflows/tests.yml/badge.svg" /></a>
  <a href="https://sonarcloud.io/summary/new_code?id=ieasybooks_tahweel" target="_blank"><img src="https://sonarcloud.io/api/project_badges/measure?project=ieasybooks_tahweel&metric=code_smells" /></a>
  <a href="https://tahweel.ieasybooks.com" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" /></a>
</div>

<div align="center">

  [![ar](https://img.shields.io/badge/lang-ar-brightgreen.svg)](README.md)
  [![en](https://img.shields.io/badge/lang-en-red.svg)](README.en.md)

</div>

# Tahweel

Convert PDF files to DOCX and TXT.

## Tahweel Features

- Convert PDF files to DOCX and TXT using Google OCR technologies
- Ability to convert a single file or an entire folder of files
- Get output with the same number of pages as the PDF file

## Requirements

- Fast internet connection since files will be uploaded to Google servers for processing
- Create Service Account Credentials from Google Cloud Platform as shown in [this link](https://developers.google.com/workspace/guides/create-credentials)
- Install Python version 3.10 or higher on your computer
- Install the `poppler-utils` library on your operating system

## Installing Tahweel

### Via `pip`

You can install Tahweel via `pip` using the command: `pip install tahweel`

### From Source Code

- Download this repository by clicking on Code then Download ZIP or by executing the following command: `git clone git@github.com:ieasybooks/tahweel.git`
- Extract the file if you downloaded it as ZIP and navigate to the project folder
- Run the following command to install Tahweel: `poetry install`

## Using Tahweel

### Available Options

- PDF file paths or directories containing multiple PDF files: You must pass file or directory paths directly after the Tahweel library name. For example: `tahweel "./pdfs"`
- Service Account Credentials file(s): You must pass the path to your `JSON` file from Google Cloud Platform (or multiple files) to the `--service-account-credentials` option
- Target file extensions: You can pass target extensions such as `.pdf` or `.jpg` to the `--file-extensions` option. The default value includes the `.pdf` extension and all image extensions supported on your computer
- Number of PDF to image conversion operations: You can specify the number through the `--pdf2image-thread-count` option. Depending on your computer's power, you can decrease or increase this value. The default value is `8`
- Number of image to text conversion operations: You can specify the number through the `--processor-max-workers` option. Depending on your internet connection quality, you can decrease or increase this value. The default value is `8`
- Output type when processing a folder of files: When processing an entire folder of PDF files, you can specify the output type by passing either `tree_to_tree` or `side_by_side` to the `--dir-output-type` option. The first value, `tree_to_tree`, will create a new folder with the same structure as the original folder for each output type (TXT and DOCX). The second value, `side_by_side`, will create TXT and DOCX files next to the PDF files inside the original folder. The default value is `tree_to_tree`
- Page separator in TXT files: You can specify the text that separates pages in TXT files through the `--txt-page-separator` option. The default value is `PAGE_SEPARATOR`
- Remove lines from DOCX files: You can remove lines from DOCX files before writing content through the `--docx-remove-newlines` option, which is useful if you want the number of pages in the DOCX file to be equal to the number of pages in the PDF file. The default value is `False`
- Output formats: You can specify the output format through the `--output-formats` option. Available formats:
  - `txt`
  - `docx`
- Output directory: You can specify the output directory through the `--output-dir` option. If you don't specify an output directory, the outputs will be written based on the file and directory paths you gave to Tahweel

```
➜ tahweel --help
usage: tahweel --service-account-credentials SERVICE_ACCOUNT_CREDENTIALS [SERVICE_ACCOUNT_CREDENTIALS ...] [--file-extensions FILE_EXTENSIONS [FILE_EXTENSIONS ...]]
               [--pdf2image-thread-count PDF2IMAGE_THREAD_COUNT] [--processor-max-workers PROCESSOR_MAX_WORKERS] [--dir-output-type {tree_to_tree,side_by_side}]
               [--txt-page-separator TXT_PAGE_SEPARATOR] [--docx-remove-newlines] [--output-formats {txt,docx} [{txt,docx} ...]] [--output-dir OUTPUT_DIR] [--skip-output-check] [-h] [--version]
               files_or_dirs_paths [files_or_dirs_paths ...]

positional arguments:
  files_or_dirs_paths   Path to the file or directory to be processed.

options:
  --service-account-credentials SERVICE_ACCOUNT_CREDENTIALS [SERVICE_ACCOUNT_CREDENTIALS ...]
                        Paths to the service account credentials JSON files. Multiple credentials will enable parallel processing.
  --file-extensions FILE_EXTENSIONS [FILE_EXTENSIONS ...]
                        Custom file extensions to search for (e.g., .pdf, .jpg). If not provided, defaults to PDF and supported image formats.
  --pdf2image-thread-count PDF2IMAGE_THREAD_COUNT
                        (int, default=8) Number of threads to use for PDF to image conversion using `pdf2image` package.
  --processor-max-workers PROCESSOR_MAX_WORKERS
                        (int, default=8) Number of threads to use while performing OCR on PDF pages.
  --dir-output-type {tree_to_tree,side_by_side}
                        Use this argument when processing a directory. `tree_to_tree` means the output will be in a new directory beside the input directory with the same structure, while
                        `side_by_side` means the output will be in the same input directory beside each file.
  --txt-page-separator TXT_PAGE_SEPARATOR
                        (str, default=PAGE_SEPARATOR) Separator to use between pages in the output TXT file.
  --docx-remove-newlines
                        (bool, default=False) Remove newlines from the output DOCX file. Useful if you want DOCX and PDF to have the same page count.
  --output-formats {txt,docx} [{txt,docx} ...]
                        Format of the output files; if not specified, `txt` and `docx` formats will be produced.
  --output-dir OUTPUT_DIR
                        (pathlib._local.Path | None, default=None) Path to the output directory. This overrides the default output directory behavior.
  --skip-output-check   (bool, default=False) Use this flag in development only to skip the output check.
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

### Converting through Command Line

#### Converting a Single PDF File

```bash
tahweel "./pdfs/1.pdf" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --txt-page-separator PAGE_SEPARATOR
```

#### Converting Multiple PDF Files and Folders

```bash
tahweel "./pdfs/1.pdf" "./pdfs/2.pdf" "./other_pdfs" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --txt-page-separator PAGE_SEPARATOR
```

#### Converting an Entire Folder of Files

```bash
tahweel "./pdfs" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --dir-output-type tree_to_tree \
  --txt-page-separator PAGE_SEPARATOR \
  --docx-remove-newlines
```

### Converting through Code

You can use Tahweel through code as follows:

```python
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from tahweel.enums import TahweelType
from tahweel.managers import PdfFileManager
from tahweel.processors import GoogleDriveOcrProcessor
from tahweel.writers import DocxWriter, TxtWriter
from tqdm import tqdm


def main():
  processor = GoogleDriveOcrProcessor('./service_account_credentials.json')
  pdf_file_manager = PdfFileManager(Path('./pdfs/1.pdf'), 8)
  pdf_file_manager.to_images()

  with ThreadPoolExecutor(max_workers=8) as executor:
    content = list(
      tqdm(executor.map(processor.process, pdf_file_manager.images_paths), total=pdf_file_manager.pages_count()),
    )

  TxtWriter(pdf_file_manager.txt_file_path(TahweelType.FILE)).write(content, 'PAGE_SEPARATOR')
  DocxWriter(pdf_file_manager.docx_file_path(TahweelType.FILE)).write(content, False)


if __name__ == '__main__':
  main()
```

### Converting using Docker

If you have Docker on your computer, the easiest way to use Tahweel is through it. The following command downloads the Tahweel Docker image, converts a PDF file using Google Drive OCR technologies, and outputs the results in the current directory:

```bash
docker run -it --rm -v "$PWD:/tahweel" ghcr.io/ieasybooks/tahweel \
  "./pdfs/1.pdf" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --dir-output-type tree_to_tree \
  --txt-page-separator PAGE_SEPARATOR \
  --docx-remove-newlines
```

You can pass any option from the Tahweel library options shown above, but you must be careful to run the command from inside the directory that contains the PDF files to be converted and your Service Account Credentials file.

---

This project relied heavily on the [ocrarian.py](https://github.com/ocrarian/ocrarian.py) repository to accomplish Tahweel more quickly, may God reward those who worked on it. 