$sourceJson = 'C:\Users\Lenovo\.gemini\antigravity\brain\17b41fc8-9927-4b95-8d6b-847895c1f79f\scratch\dataset_source.json'
$targetDir  = 'C:\Users\Lenovo\.gemini\antigravity\scratch\privacy_threat_dataset'
$docsDir    = 'C:\Users\Lenovo\Documents'

$items = Get-Content $sourceJson -Raw -Encoding UTF8 | ConvertFrom-Json

$records = foreach ($it in $items) {
    $t = $it.text
    [PSCustomObject]@{
        'id'               = $it.id
        'sub_label'        = $it.sub_label
        'source'           = $it.source
        'text'             = $it.text
        'фрагмент_ИМЯ'        = if ($t.Contains('[ИМЯ]')) { '[ИМЯ]' } else { '' }
        'фрагмент_ТЕЛЕФОН'    = if ($t.Contains('[ТЕЛЕФОН]')) { '[ТЕЛЕФОН]' } else { '' }
        'фрагмент_АДРЕС'      = if ($t.Contains('[АДРЕС]')) { '[АДРЕС]' } else { '' }
        'фрагмент_EMAIL'      = if ($t.Contains('[EMAIL]')) { '[EMAIL]' } else { '' }
        'фрагмент_АККАУНТ'    = if ($t.Contains('[АККАУНТ]')) { '[АККАУНТ]' } else { '' }
        'фрагмент_ГЕОЛОКАЦИЯ' = if ($t.Contains('[ГЕОЛОКАЦИЯ]')) { '[ГЕОЛОКАЦИЯ]' } else { '' }
        'language'         = $it.language
        'is_anonymized'    = $it.is_anonymized
    }
}

$csvPath = Join-Path $targetDir 'privacy_threat_dataset.csv'
$records | Export-Csv -Path $csvPath -NoTypeInformation -Encoding utf8

$excelPath = Join-Path $targetDir 'privacy_threat_dataset_excel.csv'
$records | Export-Csv -Path $excelPath -Delimiter ';' -NoTypeInformation -Encoding utf8

$jsonlPath = Join-Path $targetDir 'privacy_threat_dataset.jsonl'
$jsonLines = $records | ForEach-Object { $_ | ConvertTo-Json -Compress }
[System.IO.File]::WriteAllLines($jsonlPath, $jsonLines, [System.Text.Encoding]::UTF8)

$docExcel = Join-Path $docsDir '2026-09-18T08-49_export_structured.csv'
$records | Export-Csv -Path $docExcel -Delimiter ';' -NoTypeInformation -Encoding utf8

Write-Host 'Done export complete.'