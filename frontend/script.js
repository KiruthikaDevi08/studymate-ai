// File upload handling
document.getElementById('fileInput').addEventListener('change', handleFileUpload);

async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        alert('Error uploading file');
    }
}
async function askQuestion() {
    const question = document.getElementById('questionInput').value;
    const answerDiv = document.getElementById('answer');
    
    if (!question) {
        answerDiv.innerHTML = "⚠️ Please enter a question";
        return;
    }

    answerDiv.innerHTML = "🤔 Thinking...";
    
    try {
        const response = await fetch('http://127.0.0.1:5000/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: question })
        });
        
        const data = await response.json();
        answerDiv.innerHTML = `💡 ${data.answer}`;
    } catch (error) {
        answerDiv.innerHTML = "❌ Error connecting to server";
    }
}