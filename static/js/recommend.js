document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const resultsInfo = document.getElementById('resultsInfo');
    const recommendationsList = document.getElementById('recommendationsList');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const query = document.getElementById('query').value;
        const model = document.getElementById('model').value;
        
        if (!query.trim()) {
            SmartCourseUtils.showToast('Please enter your learning goals', 'warning');
            return;
        }

        // Show loading
        loadingSpinner.style.display = 'block';
        resultsSection.style.display = 'none';

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    query: query,
                    model: model
                })
            });

            const data = await response.json();

            if (data.success) {
                displayResults(data);
            } else {
                throw new Error(data.error || 'Failed to get recommendations');
            }
        } catch (error) {
            console.error('Error:', error);
            SmartCourseUtils.showToast('Error getting recommendations: ' + error.message, 'danger');
        } finally {
            loadingSpinner.style.display = 'none';
        }
    });

    function displayResults(data) {
        const modelName = data.model === 'tfidf' ? 'TF-IDF' : 'Neural';
        
        resultsInfo.innerHTML = `
            <div class="alert alert-info">
                <h5>Results for: "${data.query}"</h5>
                <p class="mb-0">Model: <strong>${modelName}</strong> | Found: <strong>${data.count} courses</strong></p>
            </div>
        `;

        if (data.recommendations.length === 0) {
            recommendationsList.innerHTML = `
                <div class="alert alert-warning">
                    No courses found matching your query. Try using different keywords or a more general description.
                </div>
            `;
        } else {
            recommendationsList.innerHTML = data.recommendations.map(course => `
                <div class="card mb-3 course-card">
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-8">
                                <h5 class="card-title">${course.course_name}</h5>
                                <h6 class="card-subtitle mb-2 text-muted">
                                    ${course.department} | ${course.university}
                                </h6>
                                <p class="card-text">${course.description}</p>
                                <div class="d-flex gap-3 text-muted small">
                                    <span><i class="fas fa-signal"></i> ${course.difficulty}</span>
                                    <span><i class="fas fa-star"></i> ${course.rating}/5.0</span>
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="d-flex flex-column h-100">
                                    <div class="mb-3">
                                        <label class="form-label small">Relevance Score</label>
                                        <div class="progress" style="height: 20px;">
                                            <div class="progress-bar bg-success" 
                                                 role="progressbar" 
                                                 style="width: ${course.score_percentage}%"
                                                 aria-valuenow="${course.score_percentage}" 
                                                 aria-valuemin="0" 
                                                 aria-valuemax="100">
                                                ${course.score_percentage.toFixed(1)}%
                                            </div>
                                        </div>
                                        <div class="form-text text-end">Similarity: ${course.score.toFixed(4)}</div>
                                    </div>
                                    <button class="btn btn-outline-primary mt-auto save-course" 
                                            data-course='${JSON.stringify(course).replace(/'/g, "\\'")}'
                                            data-query="${data.query}"
                                            data-model="${data.model}">
                                        <i class="fas fa-bookmark"></i> Save Course
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');

            // Add event listeners to save buttons
            document.querySelectorAll('.save-course').forEach(button => {
                button.addEventListener('click', saveCourse);
            });
        }

        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    async function saveCourse(e) {
        const button = e.target.closest('.save-course');
        const course = JSON.parse(button.getAttribute('data-course'));
        const query = button.getAttribute('data-query');
        const model = button.getAttribute('data-model');

        try {
            const response = await fetch('/api/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    course_name: course.course_name,
                    department: course.department,
                    description: course.description,
                    model_type: model,
                    query_text: query
                })
            });

            const data = await response.json();

            if (data.success) {
                button.innerHTML = '<i class="fas fa-check"></i> Saved!';
                button.classList.remove('btn-outline-primary');
                button.classList.add('btn-success');
                button.disabled = true;
                SmartCourseUtils.showToast('Course saved successfully!', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Error saving course:', error);
            SmartCourseUtils.showToast('Error saving course: ' + error.message, 'danger');
        }
    }
});