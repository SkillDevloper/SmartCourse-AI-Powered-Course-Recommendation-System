document.addEventListener('DOMContentLoaded', function() {
    loadSearchHistory();
    loadSavedCourses();

    async function loadSearchHistory() {
        try {
            const response = await fetch('/api/history');
            const data = await response.json();

            const historyLoading = document.getElementById('historyLoading');
            const searchHistory = document.getElementById('searchHistory');

            historyLoading.style.display = 'none';

            if (data.history.length === 0) {
                searchHistory.innerHTML = '<p class="text-muted">No search history yet.</p>';
                return;
            }

            searchHistory.innerHTML = data.history.map(item => `
                <div class="card mb-2">
                    <div class="card-body py-2">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>"${item.query_text}"</strong>
                                <span class="badge bg-${item.model_type === 'tfidf' ? 'success' : 'info'} ms-2">
                                    ${item.model_type.toUpperCase()}
                                </span>
                            </div>
                            <div class="text-end">
                                <small class="text-muted">${SmartCourseUtils.formatDate(item.timestamp)}</small>
                                <br>
                                <button class="btn btn-sm btn-outline-primary mt-1 compare-search" 
                                        data-query="${item.query_text}">
                                    <i class="fas fa-balance-scale"></i> Compare
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('');

            // Add event listeners to compare buttons
            document.querySelectorAll('.compare-search').forEach(button => {
                button.addEventListener('click', function() {
                    const query = this.getAttribute('data-query');
                    compareModels(query);
                });
            });

        } catch (error) {
            console.error('Error loading history:', error);
            document.getElementById('searchHistory').innerHTML = 
                '<div class="alert alert-danger">Error loading search history</div>';
        }
    }

    async function loadSavedCourses() {
        try {
            const response = await fetch('/api/saved-courses');
            const data = await response.json();

            const savedLoading = document.getElementById('savedLoading');
            const savedCourses = document.getElementById('savedCourses');

            savedLoading.style.display = 'none';

            if (data.saved_courses.length === 0) {
                savedCourses.innerHTML = '<p class="text-muted">No saved courses yet.</p>';
                return;
            }

            // Group by query
            const grouped = {};
            data.saved_courses.forEach(course => {
                if (!grouped[course.query_text]) {
                    grouped[course.query_text] = [];
                }
                grouped[course.query_text].push(course);
            });

            savedCourses.innerHTML = Object.entries(grouped).map(([query, courses]) => `
                <div class="card mb-3">
                    <div class="card-header bg-light">
                        <h6 class="mb-0">"${query}"</h6>
                    </div>
                    <div class="card-body">
                        ${courses.map(course => `
                            <div class="border-start border-3 border-${course.model_type === 'tfidf' ? 'success' : 'info'} ps-3 mb-2">
                                <div class="d-flex justify-content-between">
                                    <div>
                                        <strong>${course.course_name}</strong>
                                        <span class="badge bg-${course.model_type === 'tfidf' ? 'success' : 'info'} ms-2">
                                            ${course.model_type.toUpperCase()}
                                        </span>
                                        <br>
                                        <small class="text-muted">${course.department}</small>
                                    </div>
                                    <small class="text-muted">${SmartCourseUtils.formatDate(course.timestamp)}</small>
                                </div>
                                <p class="small mb-0 mt-1">${course.description}</p>
                            </div>
                        `).join('')}
                    </div>
                </div>
            `).join('');

        } catch (error) {
            console.error('Error loading saved courses:', error);
            document.getElementById('savedCourses').innerHTML = 
                '<div class="alert alert-danger">Error loading saved courses</div>';
        }
    }

    async function compareModels(query) {
        const comparisonSection = document.getElementById('comparisonSection');
        comparisonSection.innerHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Comparing models for: "${query}"</p>
            </div>
        `;

        try {
            // Get recommendations from both models
            const [tfidfResponse, neuralResponse] = await Promise.all([
                fetch('/api/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, model: 'tfidf' })
                }),
                fetch('/api/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query, model: 'neural' })
                })
            ]);

            const tfidfData = await tfidfResponse.json();
            const neuralData = await neuralResponse.json();

            displayComparison(query, tfidfData, neuralData);

        } catch (error) {
            console.error('Error comparing models:', error);
            comparisonSection.innerHTML = `
                <div class="alert alert-danger">
                    Error comparing models: ${error.message}
                </div>
            `;
        }
    }

    function displayComparison(query, tfidfData, neuralData) {
        const comparisonSection = document.getElementById('comparisonSection');
        
        comparisonSection.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-success text-white">
                            <h5 class="mb-0">TF-IDF Model Results</h5>
                        </div>
                        <div class="card-body">
                            ${tfidfData.recommendations.slice(0, 5).map(course => `
                                <div class="border-start border-3 border-success ps-2 mb-3">
                                    <h6>${course.course_name}</h6>
                                    <p class="small mb-1">${course.department}</p>
                                    <div class="progress" style="height: 10px;">
                                        <div class="progress-bar bg-success" 
                                             style="width: ${course.score_percentage}%">
                                        </div>
                                    </div>
                                    <small class="text-muted">Score: ${course.score.toFixed(4)}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header bg-info text-white">
                            <h5 class="mb-0">Neural Model Results</h5>
                        </div>
                        <div class="card-body">
                            ${neuralData.recommendations.slice(0, 5).map(course => `
                                <div class="border-start border-3 border-info ps-2 mb-3">
                                    <h6>${course.course_name}</h6>
                                    <p class="small mb-1">${course.department}</p>
                                    <div class="progress" style="height: 10px;">
                                        <div class="progress-bar bg-info" 
                                             style="width: ${course.score_percentage}%">
                                        </div>
                                    </div>
                                    <small class="text-muted">Score: ${course.score.toFixed(4)}</small>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
            <div class="row mt-3">
                <div class="col-12">
                    <div class="alert alert-secondary">
                        <h6>Comparison Analysis:</h6>
                        <ul class="mb-0">
                            <li><strong>TF-IDF</strong> focuses on keyword matches in "${query}"</li>
                            <li><strong>Neural</strong> understands semantic meaning and context</li>
                            <li>Average TF-IDF score: ${(tfidfData.recommendations.reduce((sum, c) => sum + c.score, 0) / tfidfData.recommendations.length).toFixed(4)}</li>
                            <li>Average Neural score: ${(neuralData.recommendations.reduce((sum, c) => sum + c.score, 0) / neuralData.recommendations.length).toFixed(4)}</li>
                        </ul>
                    </div>
                </div>
            </div>
        `;
    }
});