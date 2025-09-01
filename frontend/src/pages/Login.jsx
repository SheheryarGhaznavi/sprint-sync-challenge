import React, { Component } from 'react'
import { Button, Container, Form, Header, Icon, Input, Loader, Message, Segment } from 'semantic-ui-react'
import api from '../services/api'

class Login extends Component
{
    constructor(props)
    {
        super(props)
        this.state = {
            email: '',
            password: '',
            error: '',
            loading: false, // Indicates if an API call is in progress
            notification: null // Holds notification message and type
        }
    }

    // Called after component mounts, checks if user is already logged in
    componentDidMount() {

        const token = localStorage.getItem('token')
        const user = localStorage.getItem('user')

        // If both token and user exist, redirect to home
        if (token && user) {
            window.location.href = '/'
        }
    }


    // Handles login form submission
    handleSubmit = async (e) => {

        e.preventDefault()
        this.setState({ error: '', notification: null, loading: true })
        const { email, password } = this.state

        // Checks if both email and password are provided
        if (!email || !password) {
            this.setState({ error: 'Email and password are required', loading: false })
            return
        }

        try {

            const form = new URLSearchParams()
            form.append('username', email)
            form.append('password', password)

            const { data } = await api.post('/auth/login', form, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })

            // Checks if API returned error
            if (data.error) {
                this.setState({ error: data.message, notification: { type: 'error', message: data.message }, loading: false })

            } else {

                localStorage.setItem('token', data.access_token)
                localStorage.setItem('user', JSON.stringify(data.user))
                this.setState({ notification: { type: 'success', message: 'Login successful! Redirecting...' }, loading: false })
                setTimeout(() => { window.location.href = '/' }, 1200)
            }

        } catch (err) {

            this.setState({ error: 'Network error, please try again', notification: { type: 'error', message: 'Network error, please try again' }, loading: false })
        }
    }


    render()
    {
        const { email, password, error, loading, notification } = this.state

        return (
            <Container style={{ maxWidth: 420, marginTop: 60 }}>
                <Header as='h2' textAlign='center' style={{ marginBottom: 24 }}>
                    <Icon name="tasks" color="blue" /> SprintSync Login
                </Header>
                {/* Notification message */}
                {notification && (
                    <Message
                        positive={notification.type === 'success'}
                        negative={notification.type === 'error'}
                        content={notification.message}
                        onDismiss={() => this.setState({ notification: null })}
                        style={{ marginBottom: 16 }}
                    />
                )}
                {/* Loader spinner for API calls */}
                {loading && (
                    <Loader active inline="centered" size="large" style={{ marginBottom: 16 }}>
                        Loading...
                    </Loader>
                )}
                <Segment raised style={{ borderRadius: 12, boxShadow: '0 2px 12px #eee' }}>
                    <Form onSubmit={this.handleSubmit} size="large">
                        <Form.Field>
                            <label>Email</label>
                            <Input type='email' value={email} onChange={e => this.setState({ email: e.target.value })} required maxLength={255} icon='user' iconPosition='left' placeholder='Enter your email...' />
                        </Form.Field>
                        <Form.Field>
                            <label>Password</label>
                            <Input type='password' value={password} onChange={e => this.setState({ password: e.target.value })} required minLength={8} maxLength={128} icon='lock' iconPosition='left' placeholder='Enter your password...' />
                        </Form.Field>
                        {/* Shows error message if login fails */}
                        {error && <Message negative content={error} style={{ marginBottom: 8 }} />}
                        <Button fluid primary type='submit' loading={loading} disabled={loading} size="large" style={{ marginTop: 8 }}>Login</Button>
                    </Form>
                </Segment>
            </Container>
        )
    }
}

export default Login
