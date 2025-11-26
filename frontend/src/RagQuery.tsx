import React, { useState, ChangeEvent, KeyboardEvent } from 'react';

interface ResultRow {
  [key: string]: any;
}

interface QueryResponse {
  sql: string;
  results: ResultRow[];
  insights: string;
  explanation: string;
  optimization: string;
  execution_time_ms: number;
}

const RagQuery: React.FC = () => {
  const [question, setQuestion] = useState<string>('');
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [sessionId] = useState<string>(`session-${Date.now()}`);
  const [apiKey, setApiKey] = useState<string>('');
  const [showApiKey, setShowApiKey] = useState<boolean>(false);

  const exampleQuestions = [
    'Show me the top 5 customers by total purchase amount',
    'List products with prices above $100',
    'Which customer has the highest total purchase?',
    'Show top 5 best-selling products',
    'How many orders were placed this year?',
    'Now filter them to California only', // Tests context retention!
  ];

  const handleQuery = async () => {
    if (!question.trim()) return;

    if (!apiKey.trim()) {
      setError('Please enter your OpenAI API key first!');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const res = await fetch('http://127.0.0.1:8000/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question,
          session_id: sessionId,
          api_key: apiKey,
        }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || 'Network response was not ok');
      }

      const data: QueryResponse = await res.json();
      setResponse(data);
    } catch (err: any) {
      console.error('Error querying RAG backend:', err);
      setError(
        err.message || 'Failed to fetch results. Please check if the backend is running.'
      );
    }

    setLoading(false);
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleQuery();
    }
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '40px 20px',
      }}
    >
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {/* Header */}
        <div
          style={{ textAlign: 'center', color: 'white', marginBottom: '40px' }}
        >
          <h1 style={{ fontSize: '2.5rem', marginBottom: '8px' }}>
            🤖 SQL Query Buddy
          </h1>
          <p style={{ fontSize: '1.1rem', opacity: 0.9 }}>
            RAG-Powered Conversational AI for Smart Data Insights
          </p>
          <p style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '8px' }}>
            ✨ With Conversation Memory • Query Optimization • AI Explanations
          </p>
        </div>

        {/* Main Card */}
        <div
          style={{
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
            overflow: 'hidden',
          }}
        >
          {/* Input Section */}
          <div style={{ padding: '32px', background: '#f8f9fa' }}>
            {/* API Key Input */}
            <div style={{ marginBottom: '20px', padding: '16px', background: '#fef3c7', borderRadius: '12px', border: '2px solid #f59e0b' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '8px' }}>
                <span style={{ fontSize: '16px', fontWeight: 600, color: '#92400e' }}>🔑 OpenAI API Key:</span>
                <button
                  onClick={() => setShowApiKey(!showApiKey)}
                  style={{
                    padding: '4px 12px',
                    fontSize: '12px',
                    background: 'white',
                    border: '1px solid #f59e0b',
                    borderRadius: '6px',
                    cursor: 'pointer',
                    color: '#92400e'
                  }}
                >
                  {showApiKey ? 'Hide' : 'Show'}
                </button>
              </div>
              <input
                type={showApiKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  setApiKey(e.target.value)
                }
                placeholder='Enter your OpenAI API key (sk-...)'
                style={{
                  width: '100%',
                  padding: '12px',
                  fontSize: '14px',
                  border: '2px solid #f59e0b',
                  borderRadius: '8px',
                  outline: 'none',
                  fontFamily: 'monospace',
                  background: 'white'
                }}
              />
              <p style={{ fontSize: '12px', color: '#92400e', marginTop: '8px', marginBottom: 0 }}>
                💡 Your API key is only used for this session and never stored. Get your key at: <a href="https://platform.openai.com/api-keys" target="_blank" rel="noopener noreferrer" style={{ color: '#92400e', textDecoration: 'underline' }}>platform.openai.com/api-keys</a>
              </p>
            </div>

            <div style={{ display: 'flex', gap: '12px', marginBottom: '20px' }}>
              <input
                type='text'
                value={question}
                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                  setQuestion(e.target.value)
                }
                onKeyPress={handleKeyPress}
                placeholder='Ask a question about your database...'
                disabled={loading}
                style={{
                  flex: 1,
                  padding: '16px',
                  fontSize: '16px',
                  border: '2px solid #e5e7eb',
                  borderRadius: '12px',
                  outline: 'none',
                }}
              />
              <button
                onClick={handleQuery}
                disabled={loading || !question.trim() || !apiKey.trim()}
                style={{
                  padding: '16px 32px',
                  fontSize: '16px',
                  fontWeight: 600,
                  color: 'white',
                  background:
                    loading || !question.trim() || !apiKey.trim()
                      ? '#9ca3af'
                      : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none',
                  borderRadius: '12px',
                  cursor:
                    loading || !question.trim() || !apiKey.trim() ? 'not-allowed' : 'pointer',
                }}
              >
                {loading ? 'Processing...' : 'Ask'}
              </button>
            </div>

            {/* Example Questions */}
            <div>
              <p
                style={{
                  fontSize: '14px',
                  color: '#6b7280',
                  marginBottom: '12px',
                  fontWeight: 500,
                }}
              >
                Try these examples:
              </p>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {exampleQuestions.map((example, idx) => (
                  <button
                    key={idx}
                    onClick={() => setQuestion(example)}
                    disabled={loading}
                    style={{
                      padding: '8px 16px',
                      fontSize: '13px',
                      color: '#667eea',
                      background: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                      cursor: loading ? 'not-allowed' : 'pointer',
                    }}
                  >
                    {example}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Results Section */}
          <div style={{ padding: '32px' }}>
            {error && (
              <div
                style={{
                  padding: '16px',
                  background: '#fee',
                  border: '2px solid #fcc',
                  borderRadius: '12px',
                  color: '#c33',
                  marginBottom: '24px',
                }}
              >
                {error}
              </div>
            )}

            {response && (
              <>
                {/* SQL Query */}
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{ marginBottom: '12px', color: '#333' }}>
                    🔍 Generated SQL Query
                  </h3>
                  <pre
                    style={{
                      padding: '16px',
                      background: '#1f2937',
                      color: '#10b981',
                      borderRadius: '12px',
                      overflow: 'auto',
                      fontSize: '14px',
                    }}
                  >
                    {response.sql}
                  </pre>
                  <p
                    style={{
                      fontSize: '12px',
                      color: '#6b7280',
                      marginTop: '8px',
                    }}
                  >
                    ⚡ Executed in {response.execution_time_ms.toFixed(2)}ms
                  </p>
                </div>

                {/* Explanation */}
                <div
                  style={{
                    marginBottom: '24px',
                    padding: '16px',
                    background: '#eff6ff',
                    borderLeft: '4px solid #3b82f6',
                    borderRadius: '8px',
                  }}
                >
                  <h3
                    style={{
                      marginBottom: '8px',
                      color: '#1e40af',
                      fontSize: '16px',
                    }}
                  >
                    📖 Query Explanation
                  </h3>
                  <p
                    style={{
                      color: '#1e3a8a',
                      fontSize: '14px',
                      lineHeight: '1.6',
                    }}
                  >
                    {response.explanation}
                  </p>
                </div>

                {/* Results Table */}
                <div style={{ marginBottom: '24px' }}>
                  <h3 style={{ marginBottom: '12px', color: '#333' }}>
                    📊 Results ({response.results.length} rows)
                  </h3>
                  {response.results.length > 0 && !response.results[0].error ? (
                    <div
                      style={{
                        overflowX: 'auto',
                        maxHeight: '400px',
                        overflowY: 'auto',
                      }}
                    >
                      <table
                        style={{
                          width: '100%',
                          borderCollapse: 'collapse',
                          fontSize: '14px',
                        }}
                      >
                        <thead
                          style={{
                            background: '#667eea',
                            color: 'white',
                            position: 'sticky',
                            top: 0,
                          }}
                        >
                          <tr>
                            {Object.keys(response.results[0]).map((key) => (
                              <th
                                key={key}
                                style={{
                                  padding: '12px',
                                  textAlign: 'left',
                                  fontWeight: 600,
                                }}
                              >
                                {key}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {response.results.map((row, idx) => (
                            <tr
                              key={idx}
                              style={{
                                background: idx % 2 === 0 ? 'white' : '#f9fafb',
                              }}
                            >
                              {Object.values(row).map((value, i) => (
                                <td
                                  key={i}
                                  style={{
                                    padding: '12px',
                                    borderBottom: '1px solid #e5e7eb',
                                  }}
                                >
                                  {value?.toString() || '-'}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  ) : (
                    <p style={{ color: '#6b7280' }}>No results found</p>
                  )}
                </div>

                {/* AI Insights */}
                <div
                  style={{
                    marginBottom: '24px',
                    padding: '16px',
                    background: '#fef3c7',
                    borderLeft: '4px solid #f59e0b',
                    borderRadius: '8px',
                  }}
                >
                  <h3
                    style={{
                      marginBottom: '8px',
                      color: '#92400e',
                      fontSize: '16px',
                    }}
                  >
                    💡 AI Insights
                  </h3>
                  <div
                    style={{
                      color: '#78350f',
                      fontSize: '14px',
                      lineHeight: '1.6',
                      whiteSpace: 'pre-wrap',
                    }}
                  >
                    {response.insights}
                  </div>
                </div>

                {/* Optimization Suggestions */}
                <div
                  style={{
                    padding: '16px',
                    background: '#f0fdf4',
                    borderLeft: '4px solid #10b981',
                    borderRadius: '8px',
                  }}
                >
                  <h3
                    style={{
                      marginBottom: '8px',
                      color: '#065f46',
                      fontSize: '16px',
                    }}
                  >
                    ⚡ Query Optimization
                  </h3>
                  <div
                    style={{
                      color: '#064e3b',
                      fontSize: '14px',
                      lineHeight: '1.6',
                      whiteSpace: 'pre-wrap',
                    }}
                  >
                    {response.optimization}
                  </div>
                </div>
              </>
            )}

            {!loading && !error && !response && (
              <div
                style={{
                  textAlign: 'center',
                  padding: '60px 20px',
                  color: '#9ca3af',
                }}
              >
                <p style={{ fontSize: '18px', marginBottom: '8px' }}>
                  👋 Ask a question to get started
                </p>
                <p style={{ fontSize: '14px' }}>
                  I remember our conversation, so you can ask follow-up
                  questions!
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default RagQuery;
