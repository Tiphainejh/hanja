function toggleDetails(hanja) {
    const detailsDiv = document.getElementById(`details-${hanja}`);
    if (detailsDiv) {
        // Toggle the 'visible' class
        detailsDiv.classList.toggle('visible');

        // If it's visible and data isn't loaded, fetch related words
        if (detailsDiv.classList.contains('visible') && !detailsDiv.dataset.loaded) {
            fetchRelatedWords(hanja, detailsDiv);
        }
    }
}

async function fetchRelatedWords(hanja, container) {
    try {
        // Fetch data from your server
        const response = await fetch(`/related-words?hanja=${encodeURIComponent(hanja)}`);
        const data = await response.json();

        // Check if data is not empty
        if (data.length > 0) {
            // Populate the container with the related words based on language
            container.innerHTML = data
                .map(word => {
                        return `
                        <form action="/search" method="POST" class="related-word-form">
                            <input type="hidden" name="word" value="${word.word}">
                            <button type="submit" class="related-word-button">
                                <strong>${word.word}</strong></button> (${word.hanja}) : ${word.lemma}
                            
                            </form>
                        `;
                })
                .join('');
        } else {
            // Display a message if no related words are found
            container.innerHTML = `<p>No related words found.</p>`;
        }

        // Mark as loaded to avoid re-fetching
        container.dataset.loaded = true;
    } catch (error) {
        console.error('Error fetching related words:', error);
        container.innerHTML = `<p>Error loading data.</p>`;
    }
}
