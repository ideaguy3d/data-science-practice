<?php
declare(strict_types=1);

$csvPath = __DIR__ . '/vocab_input.csv';

if (!file_exists($csvPath)) {
    http_response_code(500);
    echo 'CSV file not found.';
    exit;
}

$handle = fopen($csvPath, 'r');

if ($handle === false) {
    http_response_code(500);
    echo 'Unable to read CSV file.';
    exit;
}

$headers = fgetcsv($handle, 0, ',', '"', '\\');

if ($headers === false) {
    fclose($handle);
    http_response_code(500);
    echo 'CSV header row is missing.';
    exit;
}

$headers = array_map(static fn ($header) => trim((string) $header), $headers);

$rows = [];

while (($row = fgetcsv($handle, 0, ',', '"', '\\')) !== false) {
    if ($row === [null] || $row === false) {
        continue;
    }

    $entry = [];
    foreach ($headers as $index => $header) {
        $entry[$header] = isset($row[$index]) ? trim((string) $row[$index]) : '';
    }

    if (($entry['spanish'] ?? '') === '') {
        continue;
    }

    $rows[] = [
        'id' => $entry['id'] ?? '',
        'spanish' => $entry['spanish'],
        'english' => $entry['english'] ?? '',
        'other_common_meanings' => $entry['other_common_meanings'] ?? '',
    ];
}

fclose($handle);

?><!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Spanish Vocabulary Tooltips</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-100 min-h-screen py-12">
<main class="max-w-4xl mx-auto px-4">
    <header class="mb-10 text-center">
        <h1 class="text-3xl font-bold text-slate-900">Spanish Vocabulary</h1>
        <p class="mt-3 text-slate-600">Hover any word to see its English translation.</p>
    </header>
    <div id="app">
        <noscript>
            <p class="text-red-600 font-semibold">Please enable JavaScript to view the vocabulary list.</p>
        </noscript>
    </div>
</main>
<script>
    const vocabData = <?php echo json_encode($rows, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES); ?>;
    const app = document.getElementById('app');

    if (!Array.isArray(vocabData) || vocabData.length === 0) {
        const emptyState = document.createElement('p');
        emptyState.className = 'text-center text-slate-500';
        emptyState.textContent = 'No vocabulary entries found.';
        app.appendChild(emptyState);
    } else {
        const list = document.createElement('ul');
        list.className = 'grid gap-4 sm:grid-cols-2 md:grid-cols-4';

        vocabData.forEach((entry) => {
            const item = document.createElement('li');
            item.className = 'group relative bg-white border border-slate-200 rounded-lg px-5 py-4 shadow-sm transition-shadow hover:shadow-md';

            const word = document.createElement('span');
            word.className = 'text-lg font-semibold text-slate-900';
            word.textContent = entry.spanish;

            const tooltip = document.createElement('div');
            tooltip.className = 'absolute left-1/2 top-full z-10 mt-3 w-max max-w-xs -translate-x-1/2 rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white opacity-0 pointer-events-none transition-opacity duration-200 group-hover:opacity-100';

            const english = entry.english || 'Translation unavailable';
            tooltip.textContent = english;

            if (entry.other_common_meanings) {
                const extra = document.createElement('div');
                extra.className = 'mt-2 text-xs text-slate-200';
                extra.textContent = entry.other_common_meanings;
                tooltip.appendChild(extra);
            }

            item.appendChild(word);
            item.appendChild(tooltip);
            list.appendChild(item);
        });

        app.appendChild(list);
    }
</script>
</body>
</html>
