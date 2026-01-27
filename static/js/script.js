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

const playButton = document.getElementById("play-button");

// Check if the playButton exists before adding the event listener
if (playButton) {
    const audio = document.getElementById("audio-player");
playButton.addEventListener("click", () => {
    if (audio.paused) {
        audio.play();
        playButton.textContent = "⏸"; // Change le bouton en pause
    } else {
        audio.pause();
        playButton.textContent = "▶"; // Remet l'icône play
    }
});
}

document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector('input[data-autocomplete="word"]');
    const suggestionList = document.querySelector(".autocomplete-list");

    if (!searchInput || !suggestionList) {
        return;
    }

    let activeIndex = -1;
    let debounceTimer = null;
    let currentController = null;

    const clearSuggestions = () => {
        suggestionList.innerHTML = "";
        suggestionList.style.display = "none";
        activeIndex = -1;
    };

    const setActiveItem = (index) => {
        const items = suggestionList.querySelectorAll("li");
        items.forEach((item, idx) => {
            item.classList.toggle("active", idx === index);
        });
    };

    const applySuggestion = (value) => {
        searchInput.value = value;
        clearSuggestions();
    };

    const fetchSuggestions = async (query) => {
        if (currentController) {
            currentController.abort();
        }
        currentController = new AbortController();

        try {
            const response = await fetch(`/autocomplete?q=${encodeURIComponent(query)}`, {
                signal: currentController.signal,
            });
            if (!response.ok) {
                clearSuggestions();
                return;
            }
            const suggestions = await response.json();
            if (!Array.isArray(suggestions) || suggestions.length === 0) {
                clearSuggestions();
                return;
            }
            suggestionList.innerHTML = "";
            suggestions.forEach((suggestion) => {
                const item = document.createElement("li");
                item.textContent = suggestion;
                item.addEventListener("mousedown", (event) => {
                    event.preventDefault();
                    applySuggestion(suggestion);
                    searchInput.closest("form").submit();
                });
                suggestionList.appendChild(item);
            });
            suggestionList.style.display = "block";
        } catch (error) {
            if (error.name !== "AbortError") {
                clearSuggestions();
            }
        }
    };

    searchInput.addEventListener("input", (event) => {
        const query = event.target.value.trim().replace(/\s+/g, "");
        if (debounceTimer) {
            clearTimeout(debounceTimer);
        }
        if (!query) {
            clearSuggestions();
            return;
        }
        debounceTimer = setTimeout(() => {
            fetchSuggestions(query);
        }, 200);
    });

    searchInput.addEventListener("keydown", (event) => {
        const items = suggestionList.querySelectorAll("li");
        if (items.length === 0) {
            return;
        }
        if (event.key === "ArrowDown") {
            event.preventDefault();
            activeIndex = (activeIndex + 1) % items.length;
            setActiveItem(activeIndex);
        } else if (event.key === "ArrowUp") {
            event.preventDefault();
            activeIndex = (activeIndex - 1 + items.length) % items.length;
            setActiveItem(activeIndex);
        } else if (event.key === "Enter" && activeIndex >= 0) {
            event.preventDefault();
            applySuggestion(items[activeIndex].textContent);
            searchInput.closest("form").submit();
        } else if (event.key === "Escape") {
            clearSuggestions();
        }
    });

    searchInput.addEventListener("blur", () => {
        setTimeout(() => {
            clearSuggestions();
        }, 150);
    });
});
