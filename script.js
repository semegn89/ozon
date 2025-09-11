// Telegram WebApp API
const tg = window.Telegram.WebApp;

// Global state
let currentUser = null;
let models = [];
let instructions = [];
let recipes = [];
let tickets = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// API Test Functions
async function testAPI() {
    const resultDiv = document.getElementById('api-result');
    resultDiv.innerHTML = 'Тестирование API...';
    resultDiv.className = 'api-result';
    
    try {
        const response = await fetch('/api/test');
        const data = await response.json();
        
        resultDiv.innerHTML = JSON.stringify(data, null, 2);
        resultDiv.className = 'api-result success';
    } catch (error) {
        resultDiv.innerHTML = `Ошибка: ${error.message}`;
        resultDiv.className = 'api-result error';
    }
}

async function loadModels() {
    const resultDiv = document.getElementById('api-result');
    resultDiv.innerHTML = 'Загрузка моделей...';
    resultDiv.className = 'api-result';
    
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        resultDiv.innerHTML = JSON.stringify(data, null, 2);
        resultDiv.className = 'api-result success';
        
        // Also update the models list
        models = data;
        displayModels();
    } catch (error) {
        resultDiv.innerHTML = `Ошибка: ${error.message}`;
        resultDiv.className = 'api-result error';
    }
}

function initializeApp() {
    // Configure Telegram WebApp
    tg.ready();
    tg.expand();
    
    // Get user data
    currentUser = tg.initDataUnsafe?.user;
    
    // Set theme colors
    document.body.style.setProperty('--tg-theme-bg-color', tg.themeParams.bg_color || '#ffffff');
    document.body.style.setProperty('--tg-theme-text-color', tg.themeParams.text_color || '#000000');
    document.body.style.setProperty('--tg-theme-hint-color', tg.themeParams.hint_color || '#999999');
    document.body.style.setProperty('--tg-theme-button-color', tg.themeParams.button_color || '#2481cc');
    document.body.style.setProperty('--tg-theme-button-text-color', tg.themeParams.button_text_color || '#ffffff');
    document.body.style.setProperty('--tg-theme-secondary-bg-color', tg.themeParams.secondary_bg_color || '#f8f9fa');
    
    // Setup event listeners
    setupEventListeners();
    
    // Load initial data
    loadData();
}

function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.addEventListener('click', function() {
            switchTab(this.dataset.tab);
        });
    });
    
    // Search functionality
    document.getElementById('search-input').addEventListener('input', function() {
        filterModels(this.value);
    });
    
    document.getElementById('instructions-search').addEventListener('input', function() {
        filterInstructions(this.value);
    });
    
    document.getElementById('recipes-search').addEventListener('input', function() {
        filterRecipes(this.value);
    });
    
    // Support ticket creation
    document.getElementById('create-ticket').addEventListener('click', createTicket);
    
    // Modal close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            closeModal();
        });
    });
    
    // Close modal on outside click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    });
}

function switchTab(tabName) {
    // Update tab buttons
    document.querySelectorAll('.nav-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Load tab-specific data
    switch(tabName) {
        case 'models':
            loadModels();
            break;
        case 'instructions':
            loadInstructions();
            break;
        case 'recipes':
            loadRecipes();
            break;
        case 'support':
            loadTickets();
            break;
    }
}

async function loadData() {
    try {
        showLoading(true);
        
        // Load all data in parallel
        await Promise.all([
            loadModels(),
            loadInstructions(),
            loadRecipes(),
            loadTickets()
        ]);
        
        showLoading(false);
    } catch (error) {
        console.error('Error loading data:', error);
        showError('Ошибка загрузки данных');
        showLoading(false);
    }
}

async function loadModels() {
    try {
        // Simulate API call - replace with actual API endpoint
        const response = await fetch('/api/models');
        if (response.ok) {
            models = await response.json();
        } else {
            // Fallback to mock data
            models = getMockModels();
        }
        renderModels();
    } catch (error) {
        console.error('Error loading models:', error);
        models = getMockModels();
        renderModels();
    }
}

async function loadInstructions() {
    try {
        const response = await fetch('/api/instructions');
        if (response.ok) {
            instructions = await response.json();
        } else {
            instructions = getMockInstructions();
        }
        renderInstructions();
    } catch (error) {
        console.error('Error loading instructions:', error);
        instructions = getMockInstructions();
        renderInstructions();
    }
}

async function loadRecipes() {
    try {
        const response = await fetch('/api/recipes');
        if (response.ok) {
            recipes = await response.json();
        } else {
            recipes = getMockRecipes();
        }
        renderRecipes();
    } catch (error) {
        console.error('Error loading recipes:', error);
        recipes = getMockRecipes();
        renderRecipes();
    }
}

async function loadTickets() {
    if (!currentUser) return;
    
    try {
        const response = await fetch(`/api/tickets?user_id=${currentUser.id}`);
        if (response.ok) {
            tickets = await response.json();
        } else {
            tickets = [];
        }
        renderTickets();
    } catch (error) {
        console.error('Error loading tickets:', error);
        tickets = [];
        renderTickets();
    }
}

function renderModels() {
    const container = document.getElementById('models-list');
    if (!models.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📱</div>
                <h3>Модели не найдены</h3>
                <p>Пока нет доступных моделей</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = models.map(model => `
        <div class="model-card fade-in" onclick="openModelModal(${model.id})">
            <div class="card-title">${model.name}</div>
            <div class="card-description">${model.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(model.created_at)}</span>
                <span class="card-badge">${model.instructions?.length || 0} инструкций</span>
            </div>
        </div>
    `).join('');
}

function renderInstructions() {
    const container = document.getElementById('instructions-list');
    if (!instructions.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📄</div>
                <h3>Инструкции не найдены</h3>
                <p>Пока нет доступных инструкций</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = instructions.map(instruction => `
        <div class="instruction-card fade-in" onclick="openInstructionModal(${instruction.id})">
            <div class="card-title">${instruction.title}</div>
            <div class="card-description">${instruction.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(instruction.created_at)}</span>
                <span class="card-badge">${instruction.type}</span>
            </div>
        </div>
    `).join('');
}

function renderRecipes() {
    const container = document.getElementById('recipes-list');
    if (!recipes.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🍳</div>
                <h3>Рецепты не найдены</h3>
                <p>Пока нет доступных рецептов</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = recipes.map(recipe => `
        <div class="recipe-card fade-in" onclick="openRecipeModal(${recipe.id})">
            <div class="card-title">${recipe.title}</div>
            <div class="card-description">${recipe.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(recipe.created_at)}</span>
                <span class="card-badge">${recipe.type}</span>
            </div>
        </div>
    `).join('');
}

function renderTickets() {
    const container = document.getElementById('tickets-list');
    const historyDiv = document.getElementById('ticket-history');
    
    if (!tickets.length) {
        historyDiv.style.display = 'none';
        return;
    }
    
    historyDiv.style.display = 'block';
    container.innerHTML = tickets.map(ticket => `
        <div class="ticket-item">
            <div class="ticket-status ${ticket.status}">${getStatusText(ticket.status)}</div>
            <div class="card-title">T-${ticket.id}</div>
            <div class="card-description">${ticket.subject || 'Без темы'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(ticket.created_at)}</span>
                <span>💬 ${ticket.messages?.length || 0} сообщений</span>
            </div>
        </div>
    `).join('');
}

function openModelModal(modelId) {
    const model = models.find(m => m.id === modelId);
    if (!model) return;
    
    document.getElementById('modal-title').textContent = model.name;
    document.getElementById('model-info').innerHTML = `
        <div class="card-description">${model.description || 'Описание отсутствует'}</div>
        <div class="card-meta">
            <span>📅 Создано: ${formatDate(model.created_at)}</span>
            <span>🏷️ ${model.tags || 'Без тегов'}</span>
        </div>
    `;
    
    // Show instructions for this model
    const modelInstructions = instructions.filter(inst => 
        inst.models && inst.models.some(m => m.id === modelId)
    );
    
    document.getElementById('model-instructions').innerHTML = `
        <h4>📄 Инструкции (${modelInstructions.length})</h4>
        ${modelInstructions.length ? 
            modelInstructions.map(inst => `
                <div class="instruction-card" onclick="openInstructionModal(${inst.id})">
                    <div class="card-title">${inst.title}</div>
                    <div class="card-description">${inst.description || 'Описание отсутствует'}</div>
                    <div class="card-meta">
                        <span class="card-badge">${inst.type}</span>
                    </div>
                </div>
            `).join('') :
            '<p>Инструкции для этой модели отсутствуют</p>'
        }
    `;
    
    // Show recipes for this model
    const modelRecipes = recipes.filter(recipe => 
        recipe.models && recipe.models.some(m => m.id === modelId)
    );
    
    document.getElementById('model-recipes').innerHTML = `
        <h4>🍳 Рецепты (${modelRecipes.length})</h4>
        ${modelRecipes.length ? 
            modelRecipes.map(recipe => `
                <div class="recipe-card" onclick="openRecipeModal(${recipe.id})">
                    <div class="card-title">${recipe.title}</div>
                    <div class="card-description">${recipe.description || 'Описание отсутствует'}</div>
                    <div class="card-meta">
                        <span class="card-badge">${recipe.type}</span>
                    </div>
                </div>
            `).join('') :
            '<p>Рецепты для этой модели отсутствуют</p>'
        }
    `;
    
    document.getElementById('model-modal').style.display = 'block';
}

function openInstructionModal(instructionId) {
    const instruction = instructions.find(i => i.id === instructionId);
    if (!instruction) return;
    
    document.getElementById('instruction-modal-title').textContent = instruction.title;
    document.getElementById('instruction-info').innerHTML = `
        <div class="card-description">${instruction.description || 'Описание отсутствует'}</div>
        <div class="card-meta">
            <span>📅 Создано: ${formatDate(instruction.created_at)}</span>
            <span class="card-badge">${instruction.type}</span>
        </div>
    `;
    
    document.getElementById('instruction-actions').innerHTML = `
        <div style="margin-top: 20px;">
            ${instruction.tg_file_id ? 
                `<button class="btn btn-primary" onclick="downloadInstruction(${instruction.id})">📥 Скачать файл</button>` :
                instruction.url ? 
                `<button class="btn btn-primary" onclick="openUrl('${instruction.url}')">🔗 Открыть ссылку</button>` :
                '<p>Файл недоступен</p>'
            }
        </div>
    `;
    
    document.getElementById('instruction-modal').style.display = 'block';
}

function openRecipeModal(recipeId) {
    const recipe = recipes.find(r => r.id === recipeId);
    if (!recipe) return;
    
    document.getElementById('recipe-modal-title').textContent = recipe.title;
    document.getElementById('recipe-info').innerHTML = `
        <div class="card-description">${recipe.description || 'Описание отсутствует'}</div>
        <div class="card-meta">
            <span>📅 Создано: ${formatDate(recipe.created_at)}</span>
            <span class="card-badge">${recipe.type}</span>
        </div>
    `;
    
    document.getElementById('recipe-actions').innerHTML = `
        <div style="margin-top: 20px;">
            ${recipe.tg_file_id ? 
                `<button class="btn btn-primary" onclick="downloadRecipe(${recipe.id})">📥 Скачать файл</button>` :
                recipe.url ? 
                `<button class="btn btn-primary" onclick="openUrl('${recipe.url}')">🔗 Открыть ссылку</button>` :
                '<p>Файл недоступен</p>'
            }
        </div>
    `;
    
    document.getElementById('recipe-modal').style.display = 'block';
}

function closeModal() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.style.display = 'none';
    });
}

function filterModels(query) {
    const filtered = models.filter(model => 
        model.name.toLowerCase().includes(query.toLowerCase()) ||
        (model.description && model.description.toLowerCase().includes(query.toLowerCase()))
    );
    
    const container = document.getElementById('models-list');
    if (!filtered.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>Ничего не найдено</h3>
                <p>Попробуйте изменить поисковый запрос</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filtered.map(model => `
        <div class="model-card fade-in" onclick="openModelModal(${model.id})">
            <div class="card-title">${model.name}</div>
            <div class="card-description">${model.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(model.created_at)}</span>
                <span class="card-badge">${model.instructions?.length || 0} инструкций</span>
            </div>
        </div>
    `).join('');
}

function filterInstructions(query) {
    const filtered = instructions.filter(instruction => 
        instruction.title.toLowerCase().includes(query.toLowerCase()) ||
        (instruction.description && instruction.description.toLowerCase().includes(query.toLowerCase()))
    );
    
    const container = document.getElementById('instructions-list');
    if (!filtered.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>Ничего не найдено</h3>
                <p>Попробуйте изменить поисковый запрос</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filtered.map(instruction => `
        <div class="instruction-card fade-in" onclick="openInstructionModal(${instruction.id})">
            <div class="card-title">${instruction.title}</div>
            <div class="card-description">${instruction.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(instruction.created_at)}</span>
                <span class="card-badge">${instruction.type}</span>
            </div>
        </div>
    `).join('');
}

function filterRecipes(query) {
    const filtered = recipes.filter(recipe => 
        recipe.title.toLowerCase().includes(query.toLowerCase()) ||
        (recipe.description && recipe.description.toLowerCase().includes(query.toLowerCase()))
    );
    
    const container = document.getElementById('recipes-list');
    if (!filtered.length) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>Ничего не найдено</h3>
                <p>Попробуйте изменить поисковый запрос</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = filtered.map(recipe => `
        <div class="recipe-card fade-in" onclick="openRecipeModal(${recipe.id})">
            <div class="card-title">${recipe.title}</div>
            <div class="card-description">${recipe.description || 'Описание отсутствует'}</div>
            <div class="card-meta">
                <span>📅 ${formatDate(recipe.created_at)}</span>
                <span class="card-badge">${recipe.type}</span>
            </div>
        </div>
    `).join('');
}

async function createTicket() {
    const message = document.getElementById('ticket-message').value.trim();
    if (!message) {
        showError('Пожалуйста, опишите вашу проблему');
        return;
    }
    
    if (!currentUser) {
        showError('Ошибка: пользователь не определен');
        return;
    }
    
    try {
        const response = await fetch('/api/tickets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: currentUser.id,
                username: currentUser.username,
                subject: message.substring(0, 100),
                message: message
            })
        });
        
        if (response.ok) {
            document.getElementById('ticket-message').value = '';
            showSuccess('Обращение создано успешно!');
            loadTickets();
        } else {
            showError('Ошибка создания обращения');
        }
    } catch (error) {
        console.error('Error creating ticket:', error);
        showError('Ошибка создания обращения');
    }
}

function downloadInstruction(instructionId) {
    // Implement download logic
    showSuccess('Скачивание началось...');
    closeModal();
}

function downloadRecipe(recipeId) {
    // Implement download logic
    showSuccess('Скачивание началось...');
    closeModal();
}

function openUrl(url) {
    tg.openLink(url);
}

function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'flex' : 'none';
    document.getElementById('main-content').style.display = show ? 'none' : 'block';
}

function showError(message) {
    tg.showAlert(message);
}

function showSuccess(message) {
    tg.showAlert(message);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function getStatusText(status) {
    const statusMap = {
        'open': 'Открыто',
        'in_progress': 'В работе',
        'closed': 'Закрыто'
    };
    return statusMap[status] || status;
}

// Mock data for development
function getMockModels() {
    return [
        {
            id: 1,
            name: "iPhone 15 Pro",
            description: "Новейший флагман от Apple с титановым корпусом",
            tags: "Apple, iPhone, Pro",
            created_at: "2024-01-15T10:00:00Z",
            instructions: []
        },
        {
            id: 2,
            name: "Samsung Galaxy S24",
            description: "Мощный Android смартфон с ИИ функциями",
            tags: "Samsung, Android, Galaxy",
            created_at: "2024-01-10T14:30:00Z",
            instructions: []
        }
    ];
}

function getMockInstructions() {
    return [
        {
            id: 1,
            title: "Настройка iPhone 15 Pro",
            description: "Пошаговая инструкция по первоначальной настройке",
            type: "PDF",
            created_at: "2024-01-15T10:00:00Z",
            models: [{ id: 1 }]
        },
        {
            id: 2,
            title: "Установка приложений на Galaxy S24",
            description: "Как установить и настроить приложения",
            type: "VIDEO",
            created_at: "2024-01-10T14:30:00Z",
            models: [{ id: 2 }]
        }
    ];
}

function getMockRecipes() {
    return [
        {
            id: 1,
            title: "Рецепт восстановления iPhone",
            description: "Как восстановить iPhone из резервной копии",
            type: "PDF",
            created_at: "2024-01-15T10:00:00Z",
            models: [{ id: 1 }]
        }
    ];
}
