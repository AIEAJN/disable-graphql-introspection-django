# disable-graphql-introspection-django
This repository demonstrates how to disable introspection on a GraphQL schema in a Django application using graphene-django. Disabling introspection can improve security by preventing clients from querying the schema structure in production environments. The example provides a simple and effective way to enhance the security of your GraphQL API.

# What is introspection?
Introspection, in the context of GraphQL and APIs in general, refers to the ability to interrogate the schema of an API to obtain information about its types, fields, requests and mutations. This allows developers to discover the structure of the API and understand how to interact with it without the need for external documentation.

# Introspection query example
```
{
  __schema {
    types {
      name
      fields {
        name
        type {
          name
          kind
        }
      }
    }
  }
}
```

# Mutation to allow introspection or not
```
mutation updateConfig {
  updateConfig(allowIntrospection: false) {
    allowIntrospection
    message
    success
  }
}
```