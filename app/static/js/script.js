document.addEventListener('DOMContentLoaded', function () {
    // Verifica se o Chart.js está carregado
    if (typeof Chart === 'undefined') {
        console.error('Chart.js não está carregado! Verifique se o script está incluído corretamente.');
        return;
    }

    // Função para definir opções globais dos gráficos para o tema escuro
    function setChartJsDefaults() {
        Chart.defaults.color = '#a3a3a3';
        Chart.defaults.borderColor = '#3c414e';
    }

    // Função para inicializar o gráfico de Receita x Despesa
    function initRevenueVsExpenseChart() {
        const ctx = document.getElementById('revenueVsExpenseChart');
        if (!ctx) {
            console.warn('Elemento revenueVsExpenseChart não encontrado');
            return;
        }

        try {
            // Verifica se os dados existem
            if (!ctx.dataset.chartdata) {
                console.error('Dados do gráfico não encontrados no dataset');
                return;
            }

            const chartData = JSON.parse(ctx.dataset.chartdata);
            console.log('Dados do gráfico de receita vs despesa:', chartData);

            // Verifica se os dados necessários estão presentes
            if (!chartData.labels || !chartData.revenues || !chartData.expenses) {
                console.error('Dados incompletos para o gráfico de receita vs despesa');
                return;
            }

            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Receitas',
                        data: chartData.revenues,
                        backgroundColor: 'rgba(52, 152, 219, 0.7)',
                        borderColor: '#3498db',
                        borderWidth: 2,
                        borderRadius: 4
                    }, {
                        label: 'Despesas',
                        data: chartData.expenses,
                        backgroundColor: 'rgba(231, 76, 60, 0.7)',
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
        } catch (error) {
            console.error('Erro ao inicializar gráfico de receita vs despesa:', error);
        }
    }

    // Função para inicializar o gráfico de Despesas por Categoria
    function initExpensesByCategoryChart() {
        const ctx = document.getElementById('expensesByCategoryChart');
        if (!ctx) {
            console.warn('Elemento expensesByCategoryChart não encontrado');
            return;
        }

        try {
            // Verifica se os dados existem
            if (!ctx.dataset.chartdata) {
                console.error('Dados do gráfico não encontrados no dataset');
                return;
            }

            const chartData = JSON.parse(ctx.dataset.chartdata);
            console.log('Dados do gráfico de despesas por categoria:', chartData);

            // Verifica se os dados necessários estão presentes
            if (!chartData.labels || !chartData.values) {
                console.error('Dados incompletos para o gráfico de despesas por categoria');
                return;
            }

            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: chartData.labels,
                    datasets: [{
                        label: 'Despesas por Categoria',
                        data: chartData.values,
                        backgroundColor: [
                            'rgba(52, 152, 219, 0.8)',
                            'rgba(26, 188, 156, 0.8)',
                            'rgba(241, 196, 15, 0.8)',
                            'rgba(230, 126, 34, 0.8)',
                            'rgba(155, 89, 182, 0.8)',
                            'rgba(231, 76, 60, 0.8)'
                        ],
                        borderColor: '#252830',
                        borderWidth: 3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    return `${label}: ${new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value)}`;
                                }
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Erro ao inicializar gráfico de despesas por categoria:', error);
        }
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
