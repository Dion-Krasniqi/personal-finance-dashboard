const App = () => {
    const [dashboardData, setDashboardData] = React.useState(null);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);
    
    const [formState, setFormState] = React.useState({description: '', amount: '', type: 'expense', });
    const [formMessage, setFormMessage] = React.useState('');
    const [formLoading, setFormLoading] = React.useState(false);

    
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
    
    
    
    React.useEffect(() => {
        fetchDashboardData();
    }, []);

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setFormState(prevState => ({...prevState, [name]:value}));
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        setFormMessage('');

        try {
            const response = await fetch('http://127.0.0.1:8000/finance/create_transaction/', {method: 'POST', headers: {
                'Content-Type':'application/json',},
                body: JSON.stringify(formState),
            });
            const result = await response.json();
            if (!response.ok) {
                throw new Error (result.error || 'Failed to create transaction.');
            }

            setFormMessage('Transaction created successfully!');
            fetchDashboardData();
            setFormState({description: '', amount: '', type: 'expense'});
            
        } catch (e) {
            console.error('Failed to create transaction:', e);
            setFormMessage(`Error: ${e.message}`);
        } finally {
            setFormLoading(false);
        }


    }



    if (loading) {
        return <div style={{ textAlign: 'center', padding: '2rem' }}>Loading dashboard...</div>;
    }

    if (error) {
        return <div style={{ textAlign: 'center', padding: '2rem', color: 'red' }}>{error}</div>;
    }

    return (
        <div style={{ padding: '2rem', fontFamily: 'sans-serif' }}>
            <h1 style={{ color: '#333' }}>Welcome, {dashboardData.user_email}</h1>
            
            <div style={{ marginBottom: '20px' }}>
                <a href="/plaid_link/">
                    <button style={{ padding: '10px', fontSize: '16px' }}>Connect Another Account</button>
                </a>
            </div>

            <p><strong>Total income: </strong>{dashboardData.income}</p>
            <p><strong>Total expenses: </strong>{dashboardData.expenses}</p>
            <p><strong>Balance: </strong>{dashboardData.balance}</p>

            <div style={{ border: '1px solid #ddd', padding: '20xp', borderRadius: '8px', marginBottom: '20px'}}> 
                <h2 style={{ marginBottom: '1rem' }}>Add a new Transaction</h2>
                <form onSubmit={handleFormSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10xpx'}}>
                    <input type="text" name="description" value={formState.description} onChange={handleFormChange} 
                    placeholder="Description" required style={{padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}/>
                    <input type="number" name="amount" value={formState.amount} onChange={handleFormChange} 
                    placeholder="Amount" required style={{padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}/>
                    <select name="type" value={formState.type} onChange={handleFormChange} 
                    placeholder="Description" required style={{padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}>
                        <option value="expense">Expense</option>
                        <option value="income">Income</option>
                    </select>
                    <button type="submit" disabled={formLoading} style={{ padding:'10px', fontSize:'16px',
                     backgroundColor: formLoading ? 'not-allowed':'pointer'}}>{formLoading? 'Submitting...':'Add Transaction'}</button>
                </form>
                {formMessage && <p style={{marginTop:'10px', color:formMessage.startsWith('Error')? 'red': 'green'}}>{formMessage}</p>}
            </div>


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
