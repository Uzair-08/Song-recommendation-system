let songsData = [];  // Initialize the songsData array

// Fetch the CSV file and parse it
fetch('real_world_songs_moods.csv')  // Ensure this is the correct path to your CSV file
    .then(response => response.text())  // Read the file as text
    .then(csvText => {
        console.log("CSV File Loaded: ", csvText);  // Debugging: Check the raw file contents
        parseCSV(csvText);  // Parse the CSV content
    })
    .catch(error => console.error('Error loading CSV:', error));

// Function to parse the CSV text
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');  // Trim to remove any leading/trailing newlines
    console.log("Total lines read from CSV:", lines.length);  // Debugging: Check number of lines
    console.log("CSV Lines: ", lines);  // Debugging: Check the raw lines

    // If the CSV file is empty or improperly formatted
    if (lines.length <= 1) {
        console.error('CSV file is empty or not formatted correctly.');
        return;  // Exit early if no valid lines
    }

    // Skip the header row and map each row into an object
    songsData = lines.slice(1).map(line => {
        const [song, artist, mood] = line.split(',');  // Correct the order to songname, artist, mood
        if (song && artist && mood) {
            console.log(`Parsed line - Song: ${song}, Artist: ${artist}, Mood: ${mood}`);
            return { song, artist, mood };  // Store the song, artist, and mood
        } else {
            console.error('Skipping invalid row:', line);
            return null;  // Skip invalid rows
        }
    }).filter(song => song !== null);  // Remove any null values caused by invalid rows

    console.log("Parsed Songs Data: ", songsData);  // Debugging: Check the parsed songsData
}

// Function to filter and display songs by mood
function filterSongs(mood) {
    console.log("Filtering songs for mood: ", mood);  // Debugging: Check the mood being filtered

    const filteredSongs = songsData.filter(song => song.mood === mood);  // Filter by mood
    console.log("Filtered Songs: ", filteredSongs);  // Debugging: Check the filtered songs

    const songListContainer = document.getElementById('song-list');
    songListContainer.innerHTML = '';  // Clear previous songs

    const songsToDisplay = filteredSongs.slice(0, 8);  // Limit to 10 songs
    console.log("Displaying Songs: ", songsToDisplay);  // Debugging: Check the songs to display

    songsToDisplay.forEach(song => {
        const songItem = document.createElement('div');
        songItem.classList.add('song-item');
        songItem.innerHTML = `
            <h3>${song.song}</h3>
            <p>by ${song.artist}</p>
        `;
        songListContainer.appendChild(songItem);
    });
}


// Get the song name input
const songInput = document.getElementById("song-name");

// Add an event listener to the button
document.getElementById("recommend-btn").addEventListener("click", async () => {
  const songName = songInput.value;

  // Fetch recommendations from the backend
  const response = await fetch("http://127.0.0.1:5000/recommend", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ song_name: songName }),
  });

  if (response.ok) {
    const data = await response.json();
    displayRecommendations(data.recommendations);
  } else {
    console.error("Error fetching recommendations");
  }
});

// Function to display recommendations
function displayRecommendations(recommendations) {
  const recommendationList = document.getElementById("recommendations-list");
  recommendationList.innerHTML = ""; // Clear previous recommendations

  recommendations.forEach((recommendation) => {
    const li = document.createElement("li");
    li.textContent = `${recommendation.track_name} by ${recommendation.artist_name}`;
    recommendationList.appendChild(li);
  });
}



