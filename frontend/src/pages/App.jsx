import React, { Component } from 'react'
import { Container, Menu, Button, Icon, Modal, Form, TextArea, Input, Dropdown, Table, Loader, Message } from 'semantic-ui-react'
import api from '../services/api'


const statusOptions = [
    { key: 'todo', value: 1, text: 'To Do' },
    { key: 'in_progress', value: 2, text: 'In Progress' },
    { key: 'done', value: 3, text: 'Done' },
]

class App extends Component
{
    constructor(props)
    {
        super(props)
        this.state = {
            user: null,
            tasks: [],
            loading: false, // Indicates if an API call is in progress
            modalOpen: false,
            form: { id: null, title: '', description: '', status: 'todo', total_minutes: 0 },
            aiDraft: '',
            notification: null // Holds notification message and type
        }
    }

    // Called after component mounts, loads user and tasks
    componentDidMount() {

        const u = JSON.parse(localStorage.getItem('user') || 'null')
        this.setState({ user: u })
        this.fetchTasks()
    }

    // Fetches tasks from API and updates state
    fetchTasks = async () => {
        this.setState({ loading: true, notification: null })

        try {
            const { data } = await api.get('/tasks')

            // Checks if API returned success and tasks array
            if (data && data.error === 0 && Array.isArray(data.data)) {
                this.setState({ tasks: data.data, notification: { type: 'success', message: 'Tasks loaded successfully.' } })
            } else {
                this.setState({ tasks: [], notification: { type: 'error', message: data && data.message ? data.message : 'Failed to fetch tasks.' } })
            }

        } catch (err) {
            this.setState({ tasks: [], notification: { type: 'error', message: 'Network error. Please try again later.' } })

        } finally {
            this.setState({ loading: false })
        }
    }

    // Logs out the user and redirects to login
    logout = () => {

        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
    }

    // Opens modal for creating a new task
    openCreate = () => {

        this.setState({
            form: { id: null, title: '', description: '', status: 'todo', total_minutes: 0 },
            aiDraft: '',
            modalOpen: true,
            notification: null
        })
    }

    // Opens modal for editing an existing task
    openEdit = (t) => {

        this.setState({
            form: { ...t },
            aiDraft: '',
            modalOpen: true,
            notification: null
        })
    }

    // Saves a new or edited task to the backend
    saveTask = async () => {
        const { form } = this.state

        const payload = {
            title: form.title,
            description: form.description,
            status: form.status,
            total_minutes: Number(form.total_minutes || 0),
        }

        this.setState({ loading: true, notification: null })

        try {
            let data

            if (form.id) {
                // Update existing task
                ({ data } = await api.put(`/tasks/${form.id}`, payload))
            } else {
                // Create new task
                ({ data } = await api.post('/tasks', payload))
            }

            // Checks if API returned error
            if (data && data.error !== 0) {
                this.setState({ notification: { type: 'error', message: data.message || 'Failed to save task.' } })
                return
            }

            this.setState({ modalOpen: false, notification: { type: 'success', message: 'Task saved successfully.' } })
            this.fetchTasks()

        } catch (err) {
            this.setState({ notification: { type: 'error', message: 'Network error. Please try again later.' } })
        } finally {
            this.setState({ loading: false })
        }
    }

    // Changes the status of a task
    changeStatus = async (t, status) => {

        this.setState({ loading: true, notification: null })

        try {
            const { data } = await api.post(`/tasks/${t.id}/status`, null, { params: { status } })

            // Checks if API returned success
            if (data && data.error === 0) {
                this.setState({
                    tasks: this.state.tasks.map(x => (x.id === t.id ? data.data : x)), // Updates the changed task
                    notification: { type: 'success', message: 'Task status updated.' }
                })

            } else {
                this.setState({ notification: { type: 'error', message: data && data.message ? data.message : 'Failed to update status.' } })
            }

        } catch (err) {
            this.setState({ notification: { type: 'error', message: 'Network error. Please try again later.' } })
        } finally {
            this.setState({ loading: false })
        }
    }

    // Deletes a task
    deleteTask = async (t) => {

        this.setState({ loading: true, notification: null })

        try {
            const { data } = await api.delete(`/tasks/${t.id}`)

            // Checks if API returned error
            if (data && data.error !== 0) {
                this.setState({ notification: { type: 'error', message: data.message || 'Failed to delete task.' } })
                return
            }

            this.setState({ notification: { type: 'success', message: 'Task deleted.' } })
            this.fetchTasks()

        } catch (err) {
            this.setState({ notification: { type: 'error', message: 'Network error. Please try again later.' } })
        } finally {
            this.setState({ loading: false })
        }
    }

    // Gets AI suggestion for task description
    suggest = async () => {
        const { form } = this.state

        // Only suggest if title is long enough 
        if (!form.title || form.title.length < 3) return

        this.setState({ loading: true, notification: null })

        try {
            const { data } = await api.post('/ai/suggest', { title: form.title })

            // Checks if API returned suggestion
            if (data && data.suggestion) {
                this.setState({ aiDraft: data.suggestion, notification: { type: 'success', message: 'AI suggestion loaded.' } })
            } else {
                this.setState({ notification: { type: 'error', message: data && data.message ? data.message : 'Failed to get AI suggestion.' } })
            }

        } catch (err) {
            this.setState({ notification: { type: 'error', message: 'Network error. Please try again later.' } })
        } finally {
            this.setState({ loading: false })
        }
    }

    render() {

        const { user, tasks, modalOpen, form, aiDraft, loading, notification } = this.state
        const isValid = form.title && form.title.length <= 120 && (form.description || '').length <= 4000

        return (
            <div className="container-fluid">
                {/* Top navigation bar */}
                <Menu attached="top" borderless size="large" className="row mx-0" style={{ boxShadow: '0 2px 8px #eee', background: 'linear-gradient(90deg, #e3f2fd 0%, #f9f9f9 100%)', borderRadius: 0 }}>
                    <Menu.Item header className="col-12 col-md-3 d-flex align-items-center" style={{ fontSize: '1.5rem', fontWeight: 700 }}>
                        <Icon name="tasks" color="blue" /> SprintSync
                    </Menu.Item>
                    <Menu.Item className="col-12 col-md-6 d-flex align-items-center justify-content-center" style={{ fontSize: '1rem' }}>Welcome <strong>{user?.email}</strong></Menu.Item>
                    <Menu.Menu position="right" className="col-12 col-md-3 d-flex justify-content-end">
                        <Menu.Item>
                            <Button onClick={this.openCreate} primary icon labelPosition="left" style={{ minWidth: 120 }}>
                                <Icon name="plus" /> New Task
                            </Button>
                        </Menu.Item>
                        <Menu.Item>
                            <Button onClick={this.logout} color="red" style={{ minWidth: 100 }}>Logout</Button>
                        </Menu.Item>
                    </Menu.Menu>
                </Menu>

                {/* Notification message */}
                {notification && (
                    <div className="row justify-content-center">
                        <div className="col-12 col-md-8">
                            <Message
                                positive={notification.type === 'success'}
                                negative={notification.type === 'error'}
                                content={notification.message}
                                onDismiss={() => this.setState({ notification: null })}
                                style={{ fontSize: '1rem', marginTop: 20 }}
                            />
                        </div>
                    </div>
                )}

                {/* Loader spinner for API calls */}
                {loading && (
                    <div className="row justify-content-center">
                        <div className="col-12 col-md-8">
                            <Loader active inline="centered" size="large" style={{ marginTop: 40 }}>
                                Loading...
                            </Loader>
                        </div>
                    </div>
                )}

                {/* Main task table - responsive and beautiful */}
                <div className="row justify-content-center">
                    <div className="col-12 col-md-10">
                        <Table compact celled striped color="blue" style={{ borderRadius: 12, boxShadow: '0 2px 16px #e3f2fd', overflowX: 'auto', background: '#fff', marginTop: 20 }}>
                            <Table.Header>
                                <Table.Row>
                                    <Table.HeaderCell style={{ fontSize: '1.1rem', fontWeight: 600 }}>Title</Table.HeaderCell>
                                    <Table.HeaderCell style={{ fontSize: '1.1rem', fontWeight: 600 }}>Status</Table.HeaderCell>
                                    <Table.HeaderCell style={{ fontSize: '1.1rem', fontWeight: 600 }}>Total Minutes</Table.HeaderCell>
                                    <Table.HeaderCell style={{ fontSize: '1.1rem', fontWeight: 600 }}>Actions</Table.HeaderCell>
                                </Table.Row>
                            </Table.Header>
                            <Table.Body>
                                {/* Iterates over tasks array to render each row */}
                                {tasks.map(t => (
                                    <Table.Row key={t.id} style={{ fontSize: '1rem' }}>
                                        <Table.Cell style={{ wordBreak: 'break-word', maxWidth: 220 }}>{t.title}</Table.Cell>
                                        <Table.Cell>
                                            <Dropdown
                                                selection
                                                options={statusOptions}
                                                value={t.status}
                                                onChange={(e, { value }) => this.changeStatus(t, value)}
                                                style={{ minWidth: 120 }}
                                            />
                                        </Table.Cell>
                                        <Table.Cell>{t.total_minutes}</Table.Cell>
                                        <Table.Cell>
                                            <Button size="small" onClick={() => this.openEdit(t)} color="blue" style={{ marginRight: 8 }}>Edit</Button>
                                            <Button size="small" negative onClick={() => this.deleteTask(t)}>Delete</Button>
                                        </Table.Cell>
                                    </Table.Row>
                                ))}
                            </Table.Body>
                        </Table>
                    </div>
                </div>

                {/* Modal for creating/editing tasks - responsive and elegant */}
                <Modal open={modalOpen} onClose={() => this.setState({ modalOpen: false })} size="small" style={{ borderRadius: 16, maxWidth: 480, margin: '0 auto' }}>
                    <Modal.Header style={{ fontSize: '1.3rem', fontWeight: 700 }}>{form.id ? 'Edit Task' : 'New Task'}</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Field required>
                                <label style={{ fontWeight: 600 }}>Title</label>
                                <Input
                                    value={form.title}
                                    maxLength={120}
                                    onChange={e => this.setState({ form: { ...this.state.form, title: e.target.value } })}
                                    style={{ fontSize: '1rem' }}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label style={{ fontWeight: 600 }}>Description</label>
                                <TextArea
                                    value={form.description}
                                    maxLength={4000}
                                    onChange={e => this.setState({ form: { ...this.state.form, description: e.target.value } })}
                                    style={{ fontSize: '1rem', minHeight: 80 }}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label style={{ fontWeight: 600 }}>Status</label>
                                <Dropdown
                                    selection
                                    options={statusOptions}
                                    value={form.status}
                                    onChange={(e, { value }) => this.setState({ form: { ...this.state.form, status: value } })}
                                    style={{ minWidth: 120 }}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label style={{ fontWeight: 600 }}>Total Minutes</label>
                                <Input type="number" min={0} value={form.total_minutes}
                                    onChange={e => this.setState({ form: { ...this.state.form, total_minutes: e.target.value } })}
                                    style={{ fontSize: '1rem' }}
                                />
                            </Form.Field>
                        </Form>
                        <Button onClick={this.suggest} icon labelPosition="left" color="yellow" style={{ marginTop: 8 }}>
                            <Icon name="lightbulb" /> AI Suggest
                        </Button>
                        {/* Shows AI suggestion if available */}
                        {aiDraft && (
                            <div style={{ marginTop: 10 }}>
                                <strong>Suggestion:</strong>
                                <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ddd', padding: 8, borderRadius: 8, background: '#f9f9f9', fontSize: '1rem' }}>{aiDraft}</div>
                                <Button size="small" onClick={() => this.setState({ form: { ...this.state.form, description: aiDraft } })} color="green" style={{ marginTop: 8 }}>Use suggestion</Button>
                            </div>
                        )}
                    </Modal.Content>
                    <Modal.Actions>
                        <Button onClick={() => this.setState({ modalOpen: false })} style={{ minWidth: 100 }}>Cancel</Button>
                        <Button primary onClick={this.saveTask} disabled={!isValid} style={{ minWidth: 100 }}>Save</Button>
                    </Modal.Actions>
                </Modal>
                {/* Responsive styles for Bootstrap */}
                <style>{`
                    @media (max-width: 200px) {
                        .ui.container, .container-fluid {
                            padding-left: 0 !important;
                            padding-right: 0 !important;
                        }
                        .ui.table {
                            font-size: 0.95rem !important;
                        }
                        .ui.modal {
                            width: 98vw !important;
                            left: 1vw !important;
                        }
                    }
                `}</style>
            </div>
        )
    }
}

export default App
