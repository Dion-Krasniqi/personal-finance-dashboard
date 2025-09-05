const App = () => {
    const [dashboardData, setDashboardData] = React.useState(null);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);

    React.useEffect(() => {
        const fetchDashboardData = async () => {
            setLoading(true);
            setError(null);
            try {
                const response = await fetch('/accounts/dashboard/');
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                setDashboardData(result);
            } catch (e) {
                console.error('Failed to fetch dashboard data:', e);
                setError('Failed to fetch dashboard data. Please check the server.');
            } finally {
                setLoading(false);
            }
        };

        fetchDashboardData();
    }, []);

    if (loading) {
        return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading dashboard...</div>;
    }

    if (error) {
        return <div style={{ textAlign: 'center', padding: '2rem', color: 'red' }}>{error}</div>;
    }

    return (
        <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
            <h1 style={{ color: '#333' }}>Welcome, {dashboardData.user_email}</h1>
            <p style={{ color: '#666' }}>This is the new React dashboard.</p>
            
            <div style={{ marginBottom: '20px' }}>
                <a href="/plaid_link/">
                    <button style={{ padding: '10px', fontSize: '16px' }}>Connect Another Account</button>
                </a>
            </div>

            <p><strong>Total income: </strong>{dashboardData.income}</p>
            <p><strong>Total expenses: </strong>{dashboardData.expenses}</p>
            <p><strong>Balance: </strong>{dashboardData.balance}</p>
            
            <h2>Transactions</h2>
            <ul>
                {dashboardData.transactions.length > 0 ? (
                    dashboardData.transactions.map(transaction => (
                        <li key={transaction.id}>
                            {transaction.date} — {transaction.type} — {transaction.description} — {transaction.amount}
                        </li>
                    ))
                ) : (
                    <li>No transactions this month.</li>
                )}
            </ul>
        </div>
    );
};

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);
root.render(React.createElement(App));
