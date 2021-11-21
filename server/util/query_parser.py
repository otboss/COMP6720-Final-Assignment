from model import ParsedQuery

def parser(sql_statement:str) -> ParsedQuery:
    crud = sql_statement.lower().split()
    crud_name = crud[0]
    
    try:
        
        if (crud_name == "delete"): #"DELETE FROM Employee WHERE eid=1"
            table_name= crud[crud.index("from")+1]
            
            if("where" in crud):
                i = crud.index("where")
                where_condition = crud[i+1:]
                where_condition =' '.join([str(elem) for elem in where_condition])
                return ParsedQuery.delete(table_name,where_condition)
            
            else:
                return ParsedQuery.delete(table_name)

        elif(crud_name=="select"):  # "Select name from student where n > b"
            
            table_name = crud[crud.index("from")+1]
            sindex = crud.index("select")
            findex= crud.index("from")
            projections = crud[sindex+1:findex]
            projections = ' '.join([str(elem) for elem in projections])
            
            if("where" in crud):
                i = crud.index("where")
                where_condition = crud[i+1:]
                where_condition = ' '.join([str(elem) for elem in where_condition])
                return ParsedQuery.select(table_name, projections, where_condition)
            
            else:
                return ParsedQuery.select(table_name, projections) 
                
        elif(crud_name == "insert"):  # "INSERT INTO Employee VALUES ( 1, Pam, Jones )"
            table_name = crud[2]
            o = crud.index("(")
            c = crud.index(")")
            values = crud[o+1:c]
            values =' '.join([str(elem) for elem in values])
            return ParsedQuery.insert(table_name, values)

        elif(crud_name == "update"): #" UPDATE Employee SET fname = Pam WHERE eid=2"
            table_name = crud[1]
            sindex = crud.index("set")
            windex= crud.index("where")
            set_conditions = crud[sindex+1:windex]
            set_conditions =' '.join([str(elem) for elem in set_conditions])
            where_condition = crud[windex+1:]
            where_condition = ' '.join([str(elem) for elem in where_condition])
            return ParsedQuery.update(table_name, set_conditions, where_condition) 

        elif (crud_name == "create"): 
            
            if (crud[1] == "index"): #"create index employee(eid)"
                table_col = crud[-1]
                o=table_col.index("(")
                c=table_col.index(")")
                table_name = table_col[0:o]
                col = table_col[o+1:c]
                return ParsedQuery.create_index(table_name, col) 
            
            elif(crud[1] == "table"): #"Create Table STUDENt ( ID INT, NAME STRING, SCHOOL STRING )"
                table_name = crud[2]
                col1 = crud[4]
                col2 = crud[6]
                col3 = crud[8]
                columns = [col1, col2, col3]
                return ParsedQuery.create_table(table_name, columns) 
            
            else:
                db_name= crud[2] #" create database student"
                return ParsedQuery.create_database(db_name) 

        elif (crud_name == "drop"):
            if(crud[1]== "table"):
                table_name = crud[2]
                return ParsedQuery.drop(table_name)

            elif(crud[1]== "database"):
                db_name = crud[2]
                return ParsedQuery.drop(db_name)
       
    except:
         raise Exception("Please input query in a form that matches the definition of the Database")
