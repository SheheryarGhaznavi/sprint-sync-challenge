
class BaseService:


    async def callFunction(self, function_name, params = []):

        error = 0
        message = "success"
        data = []

        try:
            function = getattr(self, function_name)
            data = await function(**params)

        except AttributeError:
            error = 1
            message = f"Function {function_name} not found"

        except Exception as e:
            error = 1
            message = f"Error executing function {function_name}: {e}"

        finally:

            if function_name == "login" and error == 0:
                return data

            return { "error": error, "message": message, "data": data }