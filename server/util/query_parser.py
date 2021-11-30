from model.ParsedQuery import ParsedQuery

def parser(sql_statement:str) -> ParsedQuery:
    crud = sql_statement.split()
    lowered = sql_statement.lower().split() # A lowered version of crud
    crud_name = lowered[0]
    
    try:
        
        if crud_name == "describe": #"DELETE FROM Employee WHERE eid=1"
            table_name = crud[1]
            return ParsedQuery.describe(table_name)

        elif crud_name == "delete": #"DELETE FROM Employee WHERE eid=1"
            table_name= crud[lowered.index("from")+1]
            
            if "where" in lowered:
                i = lowered.index("where")
                where_condition = crud[i+1:]
                where_condition = ' '.join([str(elem) for elem in where_condition])
                return ParsedQuery.delete(table_name,[where_condition])
            
            else:
                return ParsedQuery.delete(table_name)

        elif crud_name=="select":  # "SELECT name , school FROM students WHERE name = 'pam'" "Select name from student where n > b"
            
            table_name = crud[lowered.index("from")+1]
            sindex = lowered.index("select")
            findex = lowered.index("from")
            projections = crud[sindex+1:findex]
            if len(projections) > 1:
                projections.remove(",")
                
            if "where" in lowered:
                i = lowered.index("where")
                where_condition = crud[i+1:]
                where_condition = ' '.join([str(elem) for elem in where_condition])
                return ParsedQuery.select(table_name, projections, [where_condition])
            
            else:
                return ParsedQuery.select(table_name, projections) 
                
        elif crud_name == "insert":  # "INSERT INTO Employee VALUES ( 1, Pam, Jones )"
            table_name = crud[2]
            o = lowered.index("(")
            c = lowered.index(")")
            values = crud[o+1:c]
            values =' '.join([str(elem) for elem in values])
            return ParsedQuery.insert(table_name, values)

        elif crud_name == "update": #" UPDATE Employee SET fname = Pam WHERE eid=2"
            table_name = crud[1]
            sindex = lowered.index("set")
            if "where" in lowered:
                windex = lowered.index("where")
                set_conditions = crud[sindex+1:windex]
                field_name = set_conditions[0]
                value = set_conditions[2].replace("'", "")
                where_condition = crud[windex+1:]
                where_condition = ' '.join([str(elem) for elem in where_condition])
                return ParsedQuery.update(table_name, [field_name], [value], [where_condition]) 
            else:
                set_conditions = crud[sindex+1:]
                field_name = set_conditions[0]
                value = set_conditions[2].replace("'", "")
                return ParsedQuery.update(table_name, [field_name], [value]) 

        elif crud_name == "create": 
            
            if lowered[1] == "index": #"create index indexName on Employee(eid)"
                table_col = crud[-1]
                index_name = crud[2]
                o = table_col.index("(")
                c = table_col.index(")")
                table_name = table_col[0:o]
                col = table_col[o+1:c]
                return ParsedQuery.create_index(index_name, table_name, [col]) 
            
            elif lowered[1] == "table": #"Create Table STUDENt ( ID INT, NAME STRING, SCHOOL STRING )"
                table_name = crud[2]
                col1 = crud[4]
                col2 = crud[6]
                col3 = crud[8]
                columns = [col1, col2, col3]
                return ParsedQuery.create_table(table_name, columns) 
            
            else:
                db_name= crud[2] #" create database student"
                return ParsedQuery.create_database(db_name) 

        elif crud_name == "drop":
            if lowered[1] == "table":
                table_name = crud[2]
                return ParsedQuery.drop(None, table_name)

            elif lowered[1] == "database":
                db_name = crud[2]
                return ParsedQuery.drop(db_name)
       
    except Exception as e:
        print(str(e))
        raise Exception("Please input query in a form that matches the definition of the Database")