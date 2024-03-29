SELECT
    pdf.Heading_Topic AS Main_Heading,
    TRIM(s.value)::VARCHAR AS Sub_Heading_Separated
FROM {{ var('schema_name') }}.pdf.ptable pdf,
LATERAL FLATTEN(input => SPLIT(pdf.Sub_Headings, '|')) s
WHERE s.value IS NOT NULL AND TRIM(s.value) <> ''

