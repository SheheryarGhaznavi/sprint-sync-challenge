import React, { Component } from 'react'
import { Button, Container, Form, Header, Input, Message, Segment } from 'semantic-ui-react'
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
            loading: false
        }
    }


    componentDidMount() {

        const token = localStorage.getItem('token')
        const user = localStorage.getItem('user')

        if (token && user) {
            window.location.href = '/'
        }
    }


    handleSubmit = async (e) => {

        e.preventDefault()
        this.setState({ error: '' })
        const { email, password } = this.state

        if (!email || !password) {

            this.setState({ error: 'Email and password are required' })
            return
        }

        this.setState({ loading: true })

        try {

            const form = new URLSearchParams()
            form.append('username', email)
            form.append('password', password)

            const { data } = await api.post('/auth/login', form, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            })

            if (data.error) {
                this.setState({ error: data.message })

            } else {

                localStorage.setItem('token', data.access_token)
                localStorage.setItem('user', JSON.stringify(data.user))
                window.location.href = '/'
            }

        } catch (err) {

            if (err.response) {
                this.setState({ error: 'Invalid credentials' })
            } else {
                this.setState({ error: 'Network error, please try again' })
            }

        } finally {
            this.setState({ loading: false })
        }
    }


    render()
    {
        const { email, password, error, loading } = this.state
        
        return (
            <Container style={{ maxWidth: 420, marginTop: 60 }}>
                <Header as='h2' textAlign='center'>SprintSync Login</Header>
                <Segment>
                    <Form onSubmit={this.handleSubmit}>
                        <Form.Field>
                            <label>Email</label>
                            <Input type='email' value={email} onChange={e => this.setState({ email: e.target.value })} required maxLength={255} />
                        </Form.Field>
                        <Form.Field>
                            <label>Password</label>
                            <Input type='password' value={password} onChange={e => this.setState({ password: e.target.value })} required minLength={8} maxLength={128} />
                        </Form.Field>
                        {error && <Message negative content={error} />}
                        <Button fluid primary type='submit' loading={loading} disabled={loading}>Login</Button>
                    </Form>
                </Segment>
            </Container>
        )
    }
}

export default Login
