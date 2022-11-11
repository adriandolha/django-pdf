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
|Static Content (HTML, CSS) | :thumbsup: | :thumbsup: | no
|Dynamic Content (HTML, CSS, Javascript) | no | yes | no
|Interactive PDF | no | no | yes
|Customizations | no | no | yes
| Links | yes | yes | no
| Dynamic Charts (ChartsJS) | no | yes | no
| Tables | yes | yes | yes
| PNG | no | yes | yes
| Django Support | yes | yes | yes


## Samples
[WeasyPrint](sampples/weasyprint.pdf)
[Selenium](sampples/selenium.pdf)
[ReportLab](sampples/weasyprint.pdf)
