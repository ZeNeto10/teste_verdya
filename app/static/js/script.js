document.addEventListener('DOMContentLoaded', function () {

    // Função para definir opções globais dos gráficos para o tema escuro
    function setChartJsDefaults() {
        if (typeof Chart !== 'undefined') {
            Chart.defaults.color = '#a3a3a3'; // Cor do texto dos eixos e legendas
            Chart.defaults.borderColor = '#3c414e'; // Cor das linhas do grid
        }
    }

    // Função para inicializar o gráfico de Receita x Despesa
    function initRevenueVsExpenseChart() {
        const ctx = document.getElementById('revenueVsExpenseChart');
        if (!ctx) return;

        // Os dados virão do template do Flask
        const chartData = JSON.parse(ctx.dataset.chartdata);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels, // Ex: ['Janeiro', 'Fevereiro', ...]
                datasets: [{
                    label: 'Receitas',
                    data: chartData.revenues,
                    backgroundColor: 'rgba(52, 152, 219, 0.7)', // Cor primária com transparência
                    borderColor: '#3498db',
                    borderWidth: 2,
                    borderRadius: 4
                }, {
                    label: 'Despesas',
                    data: chartData.expenses,
                    backgroundColor: 'rgba(231, 76, 60, 0.7)', // Cor de perigo com transparência
                    borderColor: '#e74c3c',
                    borderWidth: 2,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function (value) {
                                return 'R$ ' + value.toLocaleString('pt-BR');
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                }
            }
        });
    }

    // Função para inicializar o gráfico de Despesas por Categoria
    function initExpensesByCategoryChart() {
        const ctx = document.getElementById('expensesByCategoryChart');
        if (!ctx) return;

        const chartData = JSON.parse(ctx.dataset.chartdata);
        
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: chartData.labels, // Ex: ['Custos Fixos', 'Marketing', ...]
                datasets: [{
                    label: 'Despesas por Categoria',
                    data: chartData.values,
                    backgroundColor: [ // Paleta de cores para o gráfico
                        'rgba(52, 152, 219, 0.8)',
                        'rgba(26, 188, 156, 0.8)',
                        'rgba(241, 196, 15, 0.8)',
                        'rgba(230, 126, 34, 0.8)',
                        'rgba(155, 89, 182, 0.8)',
                        'rgba(231, 76, 60, 0.8)'
                    ],
                    borderColor: '#252830', // Cor de fundo do container
                    borderWidth: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                    }
                }
            }
        });
    }
    
    // Ativa o link da sidebar correspondente à página atual
    function setActiveSidebarLink() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.sidebar-nav a');
        
        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');
            }
        });
    }


    // Executa as funções quando a página carregar
    setChartJsDefaults();
    initRevenueVsExpenseChart();
    initExpensesByCategoryChart();
    setActiveSidebarLink();

});
