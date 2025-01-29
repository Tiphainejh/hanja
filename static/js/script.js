function toggleDetails(hanja, original_word, text_language_no_related, text_language_error) {
    const detailsDiv = document.getElementById(`details-${hanja}`);
    const resultItem = detailsDiv.closest('.result-item'); // Get the parent .result-item
    if (detailsDiv) {
        // Toggle the 'visible' class on the details div
        detailsDiv.classList.toggle('visible');

        // Update the parent .result-item's 'collapsed' class
        if (detailsDiv.classList.contains('visible')) {
            resultItem.classList.remove('collapsed'); // Expanded state
        } else {
            resultItem.classList.add('collapsed'); // Collapsed state
        }

        // If it's visible and data isn't loaded, fetch related words
        if (detailsDiv.classList.contains('visible') && !detailsDiv.dataset.loaded) {
            fetchRelatedWords(hanja, detailsDiv, original_word, text_language_no_related, text_language_error);
        }
    }
}


async function fetchRelatedWords(hanja, container, originalWord, text_language_no_related, text_language_error) {
    try {
        // Fetch data from your server
        const response = await fetch(`/related-words?hanja=${encodeURIComponent(hanja)}&original_word=${encodeURIComponent(originalWord)}`);
        const data = await response.json();
        // Escape special characters to prevent XSS
        const sanitizeHTML = (str) =>
            String(str)
                .replace(/&/g, "&amp;")
                .replace(/</g, "&lt;")
                .replace(/>/g, "&gt;")
                .replace(/"/g, "&quot;")
                .replace(/'/g, "&#39;");

        // Check if data is not empty
        if (data.length > 0) {
            // Populate the container with the related words based on language
            container.innerHTML = data
                .map((word) => {
                    const sanitizedWord = sanitizeHTML(word.word);
                    const sanitizedHanja = sanitizeHTML(word.hanja);
                    const sanitizedLemma = sanitizeHTML(word.lemma);

                    return `
                        <form action="/search" method="POST" class="related-word-form">
                            <input type="hidden" name="word" value="${sanitizedWord}">
                            <button type="submit" class="related-word-button">
                                <strong>${sanitizedWord}</strong></button> (${sanitizedHanja}) : ${sanitizedLemma}
                        </form>
                    `;
                })
                .join('');
        } else {
            // Display a message if no related words are found
            container.innerHTML = `${text_language_no_related}`;
        }

        // Mark as loaded to avoid re-fetching
        container.dataset.loaded = true;
    } catch (error) {
        console.error('Error fetching related words:', error);
        container.innerHTML = `${text_language_error}`;
    }
}

