import React, { Component } from 'react'
import { Container, Menu, Button, Icon, Modal, Form, TextArea, Input, Dropdown, Table } from 'semantic-ui-react'
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
            loading: false,
            modalOpen: false,
            form: { id: null, title: '', description: '', status: 'todo', total_minutes: 0 },
            aiDraft: ''
        }
    }


    componentDidMount() {

        const u = JSON.parse(localStorage.getItem('user') || 'null')
        this.setState({ user: u })
        this.fetchTasks()
    }


    fetchTasks = async () => {
        this.setState({ loading: true })

        try {
            const { data } = await api.get('/tasks')

            // Handle backend error index and show message
            if (data && data.error === 0 && Array.isArray(data.data)) {
                this.setState({ tasks: data.data })
            } else {
                this.setState({ tasks: [] })
                alert(data && data.message ? data.message : 'Failed to fetch tasks. Please try again later.')
            }

        } catch (err) {
            this.setState({ tasks: [] })
            alert('Network error. Please try again later.')

        } finally {
            this.setState({ loading: false })
        }
    }


    logout = () => {

        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
    }


    openCreate = () => {

        this.setState({
            form: { id: null, title: '', description: '', status: 'todo', total_minutes: 0 },
            aiDraft: '',
            modalOpen: true
        })
    }


    openEdit = (t) => {

        this.setState({
            form: { ...t },
            aiDraft: '',
            modalOpen: true
        })
    }


    saveTask = async () => {
        const { form } = this.state

        const payload = {
            title: form.title,
            description: form.description,
            status: form.status,
            total_minutes: Number(form.total_minutes || 0),
        }

        try {
            let data

            if (form.id) {
                ({ data } = await api.put(`/tasks/${form.id}`, payload))
            } else {
                ({ data } = await api.post('/tasks', payload))
            }

            // Handle backend error index and show message
            if (data && data.error !== 0) {
                alert(data.message || 'Failed to save task.')
                return
            }

            this.setState({ modalOpen: false })
            this.fetchTasks()

        } catch (err) {
            alert('Network error. Please try again later.')
        }
    }


    changeStatus = async (t, status) => {

        try {
            const { data } = await api.post(`/tasks/${t.id}/status`, null, { params: { status } })

            // Handle backend error index and show message
            if (data && data.error === 0) {
                this.setState({
                    tasks: this.state.tasks.map(x => (x.id === t.id ? data.data : x)) // data.data is the updated task
                })

            } else {
                alert(data && data.message ? data.message : 'Failed to update status.')
            }

        } catch (err) {
            alert('Network error. Please try again later.')
        }
    }


    deleteTask = async (t) => {

        try {
            const { data } = await api.delete(`/tasks/${t.id}`)

            // Handle backend error index and show message
            if (data && data.error !== 0) {
                alert(data.message || 'Failed to delete task.')
                return
            }

            this.fetchTasks()

        } catch (err) {
            alert('Network error. Please try again later.')
        }
    }


    suggest = async () => {
        const { form } = this.state

        if (!form.title || form.title.length < 3) return

        try {
            const { data } = await api.post('/ai/suggest', { title: form.title })

            // Handle backend error index and show message
            if (data && data.suggestion) {
                this.setState({ aiDraft: data.suggestion })
            } else {
                alert(data && data.message ? data.message : 'Failed to get AI suggestion.')
            }

        } catch (err) {
            alert('Network error. Please try again later.')
        }
    }


    render() {

        const { user, tasks, modalOpen, form, aiDraft } = this.state
        const isValid = form.title && form.title.length <= 120 && (form.description || '').length <= 4000

        return (
            <>
                <Menu attached="top">
                    <Menu.Item header>Welcome {user?.email}</Menu.Item>
                    <Menu.Menu position="right">
                        <Menu.Item>
                            <Button onClick={this.openCreate} primary icon labelPosition="left">
                                <Icon name="plus" /> New Task
                            </Button>
                        </Menu.Item>
                        <Menu.Item>
                            <Button onClick={this.logout}>Logout</Button>
                        </Menu.Item>
                    </Menu.Menu>
                </Menu>

                <Container style={{ marginTop: 20 }}>
                    <Table compact celled striped>
                        <Table.Header>
                            <Table.Row>
                                <Table.HeaderCell>Title</Table.HeaderCell>
                                <Table.HeaderCell>Status</Table.HeaderCell>
                                <Table.HeaderCell>Total Minutes</Table.HeaderCell>
                                <Table.HeaderCell>Actions</Table.HeaderCell>
                            </Table.Row>
                        </Table.Header>
                        <Table.Body>
                            {tasks.map(t => (
                                <Table.Row key={t.id}>
                                    <Table.Cell>{t.title}</Table.Cell>
                                    <Table.Cell>
                                        <Dropdown
                                            selection
                                            options={statusOptions}
                                            value={t.status}
                                            onChange={(e, { value }) => this.changeStatus(t, value)}
                                        />
                                    </Table.Cell>
                                    <Table.Cell>{t.total_minutes}</Table.Cell>
                                    <Table.Cell>
                                        <Button size="small" onClick={() => this.openEdit(t)}>Edit</Button>
                                        <Button size="small" negative onClick={() => this.deleteTask(t)}>Delete</Button>
                                    </Table.Cell>
                                </Table.Row>
                            ))}
                        </Table.Body>
                    </Table>
                </Container>

                <Modal open={modalOpen} onClose={() => this.setState({ modalOpen: false })}>
                    <Modal.Header>{form.id ? 'Edit Task' : 'New Task'}</Modal.Header>
                    <Modal.Content>
                        <Form>
                            <Form.Field required>
                                <label>Title</label>
                                <Input
                                    value={form.title}
                                    maxLength={120}
                                    onChange={e => this.setState({ form: { ...this.state.form, title: e.target.value } })}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label>Description</label>
                                <TextArea
                                    value={form.description}
                                    maxLength={4000}
                                    onChange={e => this.setState({ form: { ...this.state.form, description: e.target.value } })}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label>Status</label>
                                <Dropdown
                                    selection
                                    options={statusOptions}
                                    value={form.status}
                                    onChange={(e, { value }) => this.setState({ form: { ...this.state.form, status: value } })}
                                />
                            </Form.Field>
                            <Form.Field>
                                <label>Total Minutes</label>
                                <Input type="number" min={0} value={form.total_minutes}
                                    onChange={e => this.setState({ form: { ...this.state.form, total_minutes: e.target.value } })}
                                />
                            </Form.Field>
                        </Form>
                        <Button onClick={this.suggest} icon labelPosition="left">
                            <Icon name="lightbulb" /> AI Suggest
                        </Button>
                        {aiDraft && (
                            <div style={{ marginTop: 10 }}>
                                <strong>Suggestion:</strong>
                                <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ddd', padding: 8, borderRadius: 4 }}>{aiDraft}</div>
                                <Button size="small" onClick={() => this.setState({ form: { ...this.state.form, description: aiDraft } })}>Use suggestion</Button>
                            </div>
                        )}
                    </Modal.Content>
                    <Modal.Actions>
                        <Button onClick={() => this.setState({ modalOpen: false })}>Cancel</Button>
                        <Button primary onClick={this.saveTask} disabled={!isValid}>Save</Button>
                    </Modal.Actions>
                </Modal>
            </>
        )
    }
}

export default App
