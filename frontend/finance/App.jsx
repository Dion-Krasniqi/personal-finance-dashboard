const App = () => {
    const [dashboardData, setDashboardData] = React.useState(null);
    const [loading, setLoading] = React.useState(true);
    const [error, setError] = React.useState(null);
    
    const [formState, setFormState] = React.useState({description: '', amount: '', type: 'expense', });
    const [formMessage, setFormMessage] = React.useState('');
    const [formLoading, setFormLoading] = React.useState(false);

    const [searchState, setSearchState] = React.useState({description: '', type: ''});
    const [isSearching, setIsSearching] = React.useState(false);

    
    const fetchDashboardData = async (searchParams = {}) => {
            setIsSearching(false);
            setError(null);
            try {
                const query = new URLSearchParams(searchParams).toString();
                const query_url = `/finance/transaction/search/?${query}`;

                const response = await fetch(query_url);
                
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
                setIsSearching(false);
            }
        };
    
    
    
    React.useEffect(() => {
        setLoading(true)
        fetchDashboardData(searchState);
    }, []);

    React.useEffect(() => {
        const handler = setTimeout(() => {
            fetchDashboardData(searchState);
        }, 200);

        return () => {
            clearTimeout(handler)
        }
    }, [searchState]);

    const handleFormChange = (e) => {
        const { name, value } = e.target;
        setFormState(prevState => ({...prevState, [name]:value}));
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setFormLoading(true);
        setFormMessage('');

        try {
            const response = await fetch('finance/transaction/create/', {method: 'POST', headers: {
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

    const handleDelete = async (transaction_id) => {
        if(!window.confirm("Are you sure you want to delete this transaction?")){
            return;
        }
        try {
            const response = await fetch(`finance/transaction/delete/${transaction_id}/`,{method:'DELETE'});
        
            const result = await response.json();
            if (!response.ok){
                throw new Error(result.error || "Failed to delete transaction.");
            }
            
            fetchDashboardData();
            setFormMessage("Transaction deleted successfully.");
        } catch (e) {
            console.errog("Failed to delete transaction", e);
            setFormMessage(`Error: ${e.message}`);
        }

    }

    const handleSearchChange = (e) => {
        const {name, value} = e.target;
        setSearchState(prevState => ({...prevState, [name]:value}));

    };



    if (loading) {
        return <div className="flex items-center justify-center min-h-screen text-gray-700">
            <p>Loading dashboard...</p>
        </div>;
    }

    if (error) {
        return <div className="flex items-center justify-center min-h-screen text-red-500">
            <p>{error}</p>
        </div>;
    }

    const formatCurrency = (amount) => {
        return new Intl.NumberFormat('en-US', {style:'currency', currency:'USD'}).format(amount);
    }

    const formatDate = (dateString) => {
        const options = { year:'numeric', month:'long', day:'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    }



    return (
        <div className="container mx-auto p-4 md:p-8 space-y-8">
            <header className="bg-white rounded-xl shadow-md p-6">
                <h1 className="text-3x1 font-bold text-gray-800">Welcome, {dashboardData.user_email}</h1>
                <p className="text-gray-600 mt-1">Your financial overview</p>
            </header>
            

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl shadow-md p-6 flex flex-col justify-between">
                    <div className="flex items-center justify-between">
                        <p className="text-lg font-medium text-gray-500">Balance</p>
                        <span className={`text-2x1 font-bold ${dashboardData.balance >=0 ? 'text-blue-600':'text-red-600'}`}>
                            {formatCurrency(dashboardData.balance)}</span>
                    </div>
                </div>
                <div className="bg-white rounded-xl shadow-md p-6 flex flex-col justify-between">
                    <div className="flex items-center justify-between">
                        <p className="text-lg font-medium text-gray-500">Total Income</p>
                        <span className="text-2x1 font-bold text-green-600">{formatCurrency(dashboardData.income)}</span>
                    </div>
                </div>
                <div className="bg-white rounded-xl shadow-md p-6 flex flex-col justify-between">
                    <div className="flex items-center justify-between">
                        <p className="text-lg font-medium text-gray-500">Total expenses</p>
                        <span className="text-2x1 font-bold text-red-600">{formatCurrency(dashboardData.expenses)}</span>
                    </div>
                </div>

            </div>
            <div className="bg-white rounded-xl shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4 text-gray-700">Filter Transcations</h2>
                <div className="flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-4">
                    <input type="text" name="description" value={searchState.description} onChange={handleSearchChange}
                    placeholder="Description" className="p-3 border border-gray-300 rounded-lg focus:outline-none 
                    focus:ring-2 focus:ring-blue-500"/>
                    <select name="type" value={searchState.type} onChange={handleSearchChange} 
                    className="p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value=''>All Types</option>
                        <option value='income'>Income</option>
                        <option value='expense'>Expense</option>
                    </select>
                </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="bg-white rounded-xl shadow-md p-6 lg:col-span-1">
                    <h2 className="text-xl font-semibold mb-4 text-gray-700">Add a New Transcation</h2>

                    <form onSubmit={handleFormSubmit} className="flex flex-col space-y-4">
                    <input type="text" name="description" value={formState.description} onChange={handleFormChange} 
                    placeholder="Description" required className="p-3 border border-gray-300 rounded-lg focus:outline-none
                    focus:ring-2 focus:blue-500"/>

                    <input type="number" name="amount" value={formState.amount} onChange={handleFormChange} 
                    placeholder="Amount" required className="p-3 border border-gray-300 rounded-lg focus:outline-none
                    focus:ring-2 focus:blue-500"/>

                    <select name="type" value={formState.type} onChange={handleFormChange} 
                    placeholder="Description" required className="p-3 border border-gray-300 rounded-lg focus:outline-none
                    focus:ring-2 focus:blue-500">
                        <option value="expense">Expense</option>
                        <option value="income">Income</option>
                    </select>

                    <button type="submit" disabled={formLoading} active={{cursor:'pointer', scale:'0.95', transition:'all 0.1s'}}
                    className={`py-3 px-4 rounded-lg font-semibold text-white transition-colors 
                    duration-200 ${formLoading ? 'bg-gray-400 cursor-not-allowed':
                    'bg-blue-600 hover:bg-blue-700'}`}>{formLoading? 'Submitting...':'Add Transaction'}</button>

                    </form>

                    {formMessage && <p className={`mt-4 text-sm font-medium ${formMessage.startsWith('Error') ? 'text-red-500':
                        'text-grenn-600'}`}>{formMessage}</p>}
                </div>
                <div className="bg-white rounded-xl shadow-md p-6 lg:col-span-2">
                    <h2 className="text-xl font-semibold mb-4 text-gray-700">Transcations</h2>
                    { isSearching && (
                        <div className="absolute inset-0 flex items-center justify-center bg-white bg-opacity-70 z-10 rounded-xl">
                            <svg className="animate-spin h-8 w-8 text-blue-500" xmlns="http://www3.org/2000/svg" fill="None" viewBox="0 0 24 24">
                                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                <path className="opacity-75" fill="currentColor" d="M4 12a8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.93813-2.647z"></path>
                            </svg>
                        </div>
                    )}
                    { dashboardData.transactions.length > 0 ? (
                        <div className="overflow-x-auto">
                            <table className="w-full text-left">
                                <thead className="text-gray-500 uppercase text-sm border-b">
                                    <tr>
                                        <th className="py-2 px-4">Date</th>
                                        <th className="py-2 px-4">Type</th>
                                        <th className="py-2 px-4">Description</th>
                                        <th className="py-2 px-4">Amount</th>
                                        <th className="py-2 px-4">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {dashboardData.transactions.map(transaction => (
                                        <tr key={transaction.id} className="border-b last:border-b-0 text-gray-700">
                                            <td className="py-2 px-4 whitespace-nowrap">{formatDate(transaction.date)}</td>
                                            <td className="py-2 px-4">
                                                <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                                                    transaction.type == 'income' ? 'bg-green-100 text-green-800':
                                                    'bg-red-100 text-red-800'}`}>{transaction.type}</span>
                                            </td>
                                            <td className="py-2 px-4">{transaction.description}</td>
                                            <td className="py-2 px-4 font-medium">{formatCurrency(transaction.amount)}</td>
                                            <td className="py-2 px-4">
                                                <button onClick={()=>handleDelete(transaction.id)}
                                                className="bg-red-500 hover:bg-red-600 text-white font-medium py-1 px-3 rounded-lg
                                                text-sm transition-colors duration-200">Delete</button>
                                            </td>
                                        </tr>
                                    ))}

                                </tbody>
                            </table>
                        </div>
                    ):(<p className="text-gray-500">No transcations this month</p>)}
                </div>

            </div>
 
        </div>
    );
};

const rootElement = document.getElementById('root');
const root = ReactDOM.createRoot(rootElement);
root.render(React.createElement(App));
