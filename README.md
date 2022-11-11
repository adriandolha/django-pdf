# Django PDF
An app to generate reports from bank statements. A bank statement entry contains the following:
- user id
- Category
- Date
- Description
- Amount

Each category is identified by name and a list of keywords. Each user is identified by id and has an email address and country.

Reports to be generated:
1. Average user expenses per country.
2. Average expenses per category.
3. Monthly expenses.
We're gonna generate the PDF report using both weasyprint and reportlab so we can compare them.

<details open>
  <summary>Architecture</summary>

![](design/architecture.png)
</details>

## Demo

## WeasyPrint vs ReportLab


|                    | WeasyPrint  | Selenium  | ReportLab                      
| ------------------ | ----------  | --------- | ---------
|Static Content (HTML, CSS) | :thumbsup: | :thumbsup: | :thumbsdown:
|Dynamic Content (HTML, CSS, Javascript) | :thumbsdown: | :thumbsup: | :thumbsdown:
|Interactive PDF | :thumbsdown: | :thumbsdown: | :thumbsup:
|Customizations | :thumbsdown: | :thumbsdown: | :thumbsup:
| Links | :thumbsup: | :thumbsup: | :thumbsdown:
| Dynamic Charts (ChartsJS) | no | :thumbsup: | :thumbsdown:
| Tables | :thumbsup: | :thumbsup: | :thumbsup:
| PNG | :thumbsdown: | :thumbsup: | :thumbsup:
| Django Support | :thumbsup: | :thumbsup: | :thumbsup:


## Samples
[WeasyPrint](sampples/weasyprint.pdf)
[Selenium](sampples/selenium.pdf)
[ReportLab](sampples/weasyprint.pdf)
