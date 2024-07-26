<div align="center">
  <a href="https://pypi.org/project/tahweel" target="_blank"><img src="https://img.shields.io/pypi/v/tahweel?label=PyPI%20Version&color=limegreen" /></a>
  <a href="https://pypi.org/project/tahweel" target="_blank"><img src="https://img.shields.io/pypi/pyversions/tahweel?color=limegreen" /></a>
  <a href="https://github.com/ieasybooks/tahweel/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/pypi/l/tahweel?color=limegreen" /></a>
  <a href="https://pepy.tech/project/tahweel" target="_blank"><img src="https://static.pepy.tech/badge/tahweel" /></a>

  <a href="https://github.com/ieasybooks/tahweel/actions/workflows/pre-commit.yml" target="_blank"><img src="https://github.com/ieasybooks/tahweel/actions/workflows/pre-commit.yml/badge.svg" /></a>
  <a href="https://sonarcloud.io/summary/new_code?id=ieasybooks_tahweel" target="_blank"><img src="https://sonarcloud.io/api/project_badges/measure?project=ieasybooks_tahweel&metric=code_smells" /></a>
  <a href="https://tahweel.ieasybooks.com" target="_blank"><img src="https://colab.research.google.com/assets/colab-badge.svg" /></a>
</div>

<h1 dir="rtl">تحويل</h1>

<p dir="rtl">تحويل ملفات PDF إلى DOCX و TXT.</p>

<h2 dir="rtl">مميزات تحويل</h2>

<ul dir="rtl">
  <li>تحويل ملفات PDF إلى DOCX و TXT باستخدام تقنيات التعرّف على الحروف من Google</li>
  <li>إمكانية تحويل ملف واحد أو مجلد كامل من الملفات</li>
  <li>الحصول على مخرجات بنفس عدد صفحات ملف PDF</li>
</ul>

<h2 dir="rtl">متطلبات الاستخدام</h2>

<ul dir="rtl">
  <li>إتصال انترنت جيد السرعة لأن الملفات ستُرفع إلى خوادم Google لتُعالج</li>
  <li>إنشاء Service Account Credentials من Google Cloud Platform كما هو موضّح <a href="https://developers.google.com/workspace/guides/create-credentials">هنا</a></li>
  <li>تثبيت لغة Python بإصدار 3.10 أو أعلى على حاسبك</li>
  <li>تثبيت مكتبة <code>poppler-utils</code> على نظام تشغيلك</li>
  <li>في حال تحويل ملفات تحتوي على صفحات بحجم أكبر من <code dir=ltr>5MB</code> يجب تثبيت مكتبة <code>bc</code> ومكتبة <code>imagemagick</code> على نظام تشغيلك</li>
</ul>

<h2 dir="rtl">تثبيت تحويل</h2>

<h3 dir="rtl">من خلال <code>pip</code></h3>

<p dir="rtl">يمكنك تثبيت تحويل من خلال <code>pip</code> باستخدام الأمر: <code dir="ltr">pip install tahweel</code></p>

<h3 dir="rtl">من خلال الشيفرة المصدرية</h3>

<ul dir="rtl">
  <li>قم بتنزيل هذا المستودع من خلال الضغط على Code ثم Download ZIP أو من خلال تنفيذ الأمر التالي: <code>git clone git@github.com:ieasybooks/tahweel.git</code></li>
  <li>قم بفك ضغط الملف إذا قمت بتنزيله بصيغة ZIP وتوجّه إلى مجلد المشروع</li>
  <li>قم بتنفيذ الأمر التالي لتثبيت تحويل: <code dir="ltr">poetry install</code></li>
</ul>

<h2 dir="rtl">استخدام تحويل</h2>

<h3 dir="rtl">الخيارات المتوفرة</h3>

<ul dir="rtl">
  <li>مسارات ملفات PDF أو مجلدات تحتوي على أكثر من ملف PDF: يجب تمرير مسارات الملفات أو المجلدات بعد اسم أداة تحويل بشكل مباشر. على سبيل المثال: <code dir="ltr">tahweel "./pdfs"</code></li>
  <li>ملف Service Account Credentials: يجب تمرير مسار ملف <code>JSON</code> الخاص بك من Google Cloud Platform إلى الاختيار <code dir="ltr">--service-account-credentials</code></li>
  <li>عدد عمليات تحويل ملف PDF إلى صور: يمكن تحديد العدد من خلال الاختيار <code dir="ltr">--pdf2image-thread-count</code>. حسب قوة حاسبك يمكن تقليل أو زيادة هذه القيمة. القيمة الافتراضية هي <code dir="ltr">8</code></li>
  <li>عدد عمليات تحويل الصور إلى نص: يمكن تحديد العدد من خلال الاختيار <code dir="ltr">--processor-max-workers</code>. حسب جودة اتصال الانترنت لديك يمكن تقليل أو زيادة هذه القيمة. القيمة الافتراضية هي <code dir="ltr">8</code></li>
  <li>نوع المخرجات عند معالجة مجلد من الملفات: عند معالجة مجلد كامل من ملفات PDF يمكنك تحديد نوع المخرجات من خلال تمرير إما <code>tree_to_tree</code> أو <code>side_by_side</code> إلى الاختيار <code dir="ltr">--dir-output-type</code>. القيمة الأولى وهي <code>tree_to_tree</code> ستقوم بإنشاء مجلد جديد بنفس ترتيب المجلد الأصلي لكل نوع من أنواع المخرجات TXT و DOCX. القيمة الثانية وهي <code>side_by_side</code> ستقوم بإنشاء ملفات TXT و DOCX بجانب ملفات PDF داخل المجلد الأصلي. القيمة الافتراضية هي <code dir="ltr">tree_to_tree</code></li>
  <li>فاصل الصفحات في ملفات TXT: يمكن تحديد النص الذي يفصل الصفحات في ملفات TXT من خلال الاختيار <code dir="ltr">--txt-page-separator</code>. القيمة الافتراضية هي <code dir="ltr">PAGE_SEPARATOR</code></li>
  <li>إزالة الأسطر من ملفات DOCX: يمكن إزالة الأسطر من ملفات DOCX قبل كتابة المحتوى من خلال الاختيار <code dir="ltr">--docx-remove-newlines</code> وهذا الأمر مفيد في حال أردت أن تكون عدد صفحات ملف DOCX مساوياً لعدد صفحات ملف PDF. القيمة الافتراضية هي <code dir="ltr">False</code></li>
  <li>
    صيغة المخرجات: يمكنك تحديد صيغة المخرجات من خلال الاختيار <code dir="ltr">--output-formats</code>. الصيغ المتوفرة:
    <ul dir="rtl">
      <li><code dir="ltr">txt</code></li>
      <li><code dir="ltr">docx</code></li>
    </ul>
  </li>
  <li>مجلد المخرجات: يمكنك تحديد مجلد الإخراج من خلال الاختيار <code dir="ltr">--output-dir</code>. إذا لم تُحدّد مجلد الإخراج ستُكتب المخرجات بناء على مسارات الملفات والمجلدات التي أعطيتها لتحويل</li>
</ul>

```
➜ tahweel --help
usage: tahweel --service-account-credentials SERVICE_ACCOUNT_CREDENTIALS [--pdf2image-thread-count PDF2IMAGE_THREAD_COUNT] [--processor-max-workers PROCESSOR_MAX_WORKERS]
               [--dir-output-type {tree_to_tree,side_by_side}] [--txt-page-separator TXT_PAGE_SEPARATOR] [--docx-remove-newlines] [--output-dir OUTPUT_DIR] [--skip-output-check] [-h] [--version]
               files_or_dirs_paths [files_or_dirs_paths ...]

positional arguments:
  files_or_dirs_paths   Path to the file or directory to be processed.

options:
  --service-account-credentials SERVICE_ACCOUNT_CREDENTIALS
                        (Path, required) Path to the service account credentials JSON file.
  --pdf2image-thread-count PDF2IMAGE_THREAD_COUNT
                        (int, default=8) Number of threads to use for PDF to image conversion using `pdf2image` package.
  --processor-max-workers PROCESSOR_MAX_WORKERS
                        (int, default=8) Number of threads to use while performing OCR on PDF pages.
  --dir-output-type {tree_to_tree,side_by_side}
                        Use this argument when processing a directory. `tree_to_tree` means the output will be in a new directory beside the input directory with the same structure, while `side_by_side`
                        means the output will be in the same input directory beside each file.
  --txt-page-separator TXT_PAGE_SEPARATOR
                        (str, default=PAGE_SEPARATOR) Separator to use between pages in the output TXT file.
  --docx-remove-newlines
                        (bool, default=False) Remove newlines from the output DOCX file. Useful if you want DOCX and PDF to have the same page count.
  --output-dir OUTPUT_DIR
                        (pathlib.Path | None, default=None) Path to the output directory. This overrides the default output directory behavior.
  --skip-output-check   (bool, default=False) Use this flag in development only to skip the output check.
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

<h3 dir="rtl">التحويل من خلال سطر الأوامر</h3>

<h4 dir="rtl">تحويل ملف PDF واحد</h4>

```bash
tahweel "./pdfs/1.pdf" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --txt-page-separator PAGE_SEPARATOR
```

<h4 dir="rtl">تحويل أكثر من ملف PDF ومجلد</h4>

```bash
tahweel "./pdfs/1.pdf" "./pdfs/2.pdf" "./other_pdfs" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --txt-page-separator PAGE_SEPARATOR
```

<h4 dir="rtl">تحويل مجلد كامل من الملفات</h4>

```bash
tahweel "./pdfs" \
  --service-account-credentials "./service_account_credentials.json" \
  --pdf2image-thread-count 8 \
  --processor-max-workers 8 \
  --dir-output-type tree_to_tree \
  --txt-page-separator PAGE_SEPARATOR \
  --docx-remove-newlines
```

<h3 dir="rtl">التحويل من خلال الشيفرة البرمجية</h3>

<p dir="rtl">يمكنك استخدام تحويل من خلال الشيفرة البرمجية كالتالي:</p>

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

<h3 dir="rtl">التحويل باستخدام Docker</h3>

<p dir="rtl">إذا كان لديك Docker على حاسبك، فالطريقة الأسهل لاستخدام تحويل هي من خلاله. الأمر التالي يقوم بتنزيل Docker image الخاصة بتحويل وتحويل ملف PDF باستخدام تقنيات Google Drive OCR وإخراج النتائج في المجلد الحالي:</p>

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

<p dir="rtl">يمكنك تمرير أي خيار من خيارات مكتبة تحويل المُوضّحة في الأعلى، ولكن يجب مُراعاة تنفيذ الأمر من داخل المجلد الذي يحتوي على ملفات PDF المراد تحويلها وملف Service Account Credentials الخاص بك.</p>

<hr>

<p dir="rtl">تم الاعتماد بشكل كبير على مستودع <a href="https://github.com/ocrarian/ocrarian.py">ocrarian.py</a> لإنجاز تحويل بشكل أسرع، فجزى الله من عمل عليه خير الجزاء.</p>