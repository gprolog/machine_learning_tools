/*
* Copyright 2013 Mozilla Foundation
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/
///<reference path='references.ts' />
var Shumway;
(function (Shumway) {
    (function (AVM2) {
        (function (Runtime) {
            var Multiname = Shumway.AVM2.ABC.Multiname;
            var Namespace = Shumway.AVM2.ABC.Namespace;
            var ClassInfo = Shumway.AVM2.ABC.ClassInfo;
            var InstanceInfo = Shumway.AVM2.ABC.InstanceInfo;
            var InstanceBindings = Shumway.AVM2.Runtime.InstanceBindings;
            var ClassBindings = Shumway.AVM2.Runtime.ClassBindings;

            var defineNonEnumerableGetterOrSetter = Shumway.ObjectUtilities.defineNonEnumerableGetterOrSetter;
            var defineNonEnumerableProperty = Shumway.ObjectUtilities.defineNonEnumerableProperty;
            var defineReadOnlyProperty = Shumway.ObjectUtilities.defineReadOnlyProperty;
            var defineNonEnumerableGetter = Shumway.ObjectUtilities.defineNonEnumerableGetter;
            var createEmptyObject = Shumway.ObjectUtilities.createEmptyObject;
            var toKeyValueArray = Shumway.ObjectUtilities.toKeyValueArray;

            var Interface = (function () {
                function Interface(classInfo) {
                    var ii = classInfo.instanceInfo;
                    release || assert(ii.isInterface());
                    this.name = ii.name;
                    this.classInfo = classInfo;
                }
                Interface.createInterface = function (classInfo) {
                    var ii = classInfo.instanceInfo;
                    release || assert(ii.isInterface());
                    if (Shumway.AVM2.Runtime.traceExecution.value) {
                        var str = "Creating Interface " + ii.name;
                        if (ii.interfaces.length) {
                            str += " implements " + ii.interfaces.map(function (name) {
                                return name.getName();
                            }).join(", ");
                        }
                        log(str);
                    }
                    var cls = new Interface(classInfo);
                    cls.interfaceBindings = new InstanceBindings(null, ii, null, null);
                    return cls;
                };

                Interface.prototype.toString = function () {
                    return "[interface " + this.name + "]";
                };

                Interface.prototype.isInstance = function (value) {
                    if (value === null || typeof value !== "object") {
                        return false;
                    }
                    release || assert(value.class.implementedInterfaces, "No 'implementedInterfaces' map found on class " + value.class);
                    var qualifiedName = Multiname.getQualifiedName(this.name);
                    return value.class.implementedInterfaces[qualifiedName] !== undefined;
                };

                Interface.prototype.trace = function (writer) {
                    writer.enter("interface " + this.name.getName());
                    writer.enter("interfaceBindings: ");
                    this.interfaceBindings.trace(writer);
                    writer.outdent();
                    writer.outdent();
                    writer.leave("}");
                };

                Interface.prototype.call = function (self, x) {
                    return x;
                };

                Interface.prototype.apply = function (self, args) {
                    return args[0];
                };
                return Interface;
            })();
            Runtime.Interface = Interface;

            /*
            * AVM2 Class
            *
            * +---------------------------------+
            * | Class Object                    |<------------------------------+
            * +---------------------------------+                               |
            * | scope                           |     D'                        |
            * | classInfo                       |     ^                         |
            * | baseClass                       |     |                         |
            * |                                 |   +---+                       |
            * | dynamicPrototype ---------------+-->| D |                       |
            * |                                 |   +---+                       |
            * |                                 |     ^                         |
            * |                                 |     | .__proto__              |
            * |                                 |   +---+                       |
            * | traitsPrototype ----------------+-->| T |                       |
            * |                                 |   +---+                       |
            * |                                 |     ^                         |
            * |                                 |     | .prototype   +-------+  |
            * | instanceConstructor             |-----+------------->| class |--+
            * |                                 |     |              +-------+
            * | instanceConstructorNoInitialize |-----+
            * | call                            |
            * | apply                           |
            * +---------------------------------+
            *
            * D  - Dynamic prototype object.
            * D' - Base class dynamic prototype object.
            * T  - Traits prototype, class traits + base class traits.
            */
            function setDefaultProperties(cls) {
                defineNonEnumerableProperty(cls.dynamicPrototype, Multiname.getPublicQualifiedName("constructor"), cls);
                defineReadOnlyProperty(cls.traitsPrototype, "class", cls);
                defineReadOnlyProperty(cls.instanceConstructor, "class", cls);
            }
            Runtime.setDefaultProperties = setDefaultProperties;

            var Class = (function () {
                function Class(name, instanceConstructor, callable) {
                    this.debugName = name;

                    if (instanceConstructor) {
                        release || assert(instanceConstructor.prototype);
                        this.instanceConstructor = instanceConstructor;
                        this.instanceConstructorNoInitialize = instanceConstructor;
                        this.hasInitialize = 0;
                        this.instanceConstructor.class = this;
                    }

                    if (!callable) {
                        callable = Shumway.AVM2.Runtime.ApplicationDomain.coerceCallable(this);
                    } else if (callable === Shumway.AVM2.Runtime.ApplicationDomain.coerceCallable) {
                        callable = Shumway.AVM2.Runtime.ApplicationDomain.coerceCallable(this);
                    }
                    defineNonEnumerableProperty(this, "call", callable.call);
                    defineNonEnumerableProperty(this, "apply", callable.apply);
                }
                Class.createClass = function (classInfo, baseClass, scope) {
                    var ci = classInfo;
                    var ii = ci.instanceInfo;
                    var domain = ci.abc.applicationDomain;
                    var className = Multiname.getName(ii.name);
                    var isNativeClass = ci.native;
                    if (isNativeClass) {
                        var buildClass = getNative(ci.native.cls);
                        if (!buildClass) {
                            Shumway.Debug.unexpected("No native for " + ci.native.cls);
                        }

                        // Special case Object, which has no base class but needs the Class class on the scope.
                        if (!baseClass) {
                            scope = new Scope(scope, Class);
                        }
                    }
                    var classScope = new Scope(scope, null);
                    var instanceConstructor = createFunction(ii.init, classScope, false);
                    var cls;
                    if (isNativeClass) {
                        cls = buildClass(domain, classScope, instanceConstructor, baseClass);
                    } else {
                        cls = new Class(className, instanceConstructor);
                    }
                    cls.className = className;
                    cls.classInfo = classInfo;
                    cls.scope = classScope;
                    classScope.object = cls;
                    var classNatives;
                    var instanceNatives;
                    if (isNativeClass) {
                        if (cls.native) {
                            classNatives = cls.native.static;
                            instanceNatives = cls.native.instance;
                        }
                    } else {
                        cls.extend(baseClass);
                    }

                    cls.classBindings = new ClassBindings(classInfo, classScope, classNatives);
                    cls.classBindings.applyTo(domain, cls);
                    defineReadOnlyProperty(cls, Shumway.AVM2.Runtime.VM_IS_CLASS, true);

                    cls.instanceBindings = new InstanceBindings(baseClass ? baseClass.instanceBindings : null, ii, classScope, instanceNatives);
                    if (cls.instanceConstructor) {
                        cls.instanceBindings.applyTo(domain, cls.traitsPrototype);
                    }

                    cls.implementedInterfaces = cls.instanceBindings.implementedInterfaces;
                    return cls;
                };

                Class.prototype.setSymbol = function (props) {
                    this.instanceConstructor.prototype.symbol = props;
                };

                Class.prototype.getSymbol = function () {
                    return this.instanceConstructor.prototype.symbol;
                };

                Class.prototype.initializeInstance = function (obj) {
                    // Initialize should be nullary and nonrecursive. If the script
                    // needs to pass in script objects to native land, there's usually a
                    // ctor function.
                    var c = this;
                    var initializes = [];
                    while (c) {
                        if (c.hasInitialize & Class.OWN_INITIALIZE) {
                            initializes.push(c.instanceConstructor.prototype.initialize);
                        }
                        c = c.baseClass;
                    }
                    var s;
                    while ((s = initializes.pop())) {
                        s.call(obj);
                    }
                    Counter.count("Initialize Instance " + obj.class);
                };

                Class.prototype.createInstance = function (args) {
                    var o = Object.create(this.instanceConstructor.prototype);
                    this.instanceConstructor.apply(o, args);
                    return o;
                };

                Class.prototype.createAsSymbol = function (props) {
                    var o = Object.create(this.instanceConstructor.prototype);

                    // Custom classes will have already have .symbol linked.
                    if (o.symbol) {
                        var symbol = Object.create(o.symbol);
                        for (var prop in props) {
                            symbol[prop] = props[prop];
                        }
                        o.symbol = symbol;
                    } else {
                        o.symbol = props;
                    }
                    return o;
                };

                Class.prototype.extendNative = function (baseClass, native) {
                    this.baseClass = baseClass;
                    this.dynamicPrototype = Object.getPrototypeOf(native.prototype);
                    this.instanceConstructor.prototype = this.traitsPrototype = native.prototype;
                    setDefaultProperties(this);
                };

                Class.prototype.extendWrapper = function (baseClass, wrapper) {
                    release || assert(this.instanceConstructor === wrapper);
                    this.baseClass = baseClass;
                    this.dynamicPrototype = Object.create(baseClass.dynamicPrototype);
                    var traitsPrototype = Object.create(this.dynamicPrototype, Shumway.ObjectUtilities.getOwnPropertyDescriptors(wrapper.prototype));
                    this.instanceConstructor.prototype = this.traitsPrototype = traitsPrototype;
                    setDefaultProperties(this);
                };

                Class.prototype.extendBuiltin = function (baseClass) {
                    release || assert(baseClass);

                    // Some natives handle their own prototypes/it's impossible to do the
                    // traits/public prototype BS, e.g. Object, Array, etc.
                    // FIXME: This is technically non-semantics preserving.
                    this.baseClass = baseClass;
                    this.dynamicPrototype = this.traitsPrototype = this.instanceConstructor.prototype;
                    setDefaultProperties(this);
                };

                Class.prototype.extend = function (baseClass) {
                    release || assert(baseClass);
                    this.baseClass = baseClass;
                    this.dynamicPrototype = Object.create(baseClass.dynamicPrototype);
                    if (baseClass.hasInitialize) {
                        var instanceConstructorNoInitialize = this.instanceConstructor;
                        var self = this;
                        this.instanceConstructor = function () {
                            self.initializeInstance(this);
                            instanceConstructorNoInitialize.apply(this, arguments);
                        };
                        defineReadOnlyProperty(this.instanceConstructor, "class", instanceConstructorNoInitialize.class);
                        this.hasInitialize |= Class.SUPER_INITIALIZE;
                    }
                    this.instanceConstructor.prototype = this.traitsPrototype = Object.create(this.dynamicPrototype);
                    setDefaultProperties(this);
                };

                Class.prototype.setDefaultProperties = function () {
                    setDefaultProperties(this);
                };

                Class.prototype.link = function (definition) {
                    release || assert(definition);
                    release || assert(this.dynamicPrototype);

                    if (definition.initialize) {
                        if (!this.hasInitialize) {
                            var instanceConstructorNoInitialize = this.instanceConstructor;
                            var self = this;
                            this.instanceConstructor = function () {
                                self.initializeInstance(this);
                                instanceConstructorNoInitialize.apply(this, arguments);
                            };
                            defineReadOnlyProperty(this.instanceConstructor, "class", instanceConstructorNoInitialize.class);
                            this.instanceConstructor.prototype = instanceConstructorNoInitialize.prototype;
                        }
                        this.hasInitialize |= Class.OWN_INITIALIZE;
                    }

                    var dynamicPrototype = this.dynamicPrototype;
                    var keys = Object.keys(definition);
                    for (var i = 0; i < keys.length; i++) {
                        var propertyName = keys[i];
                        Object.defineProperty(dynamicPrototype, propertyName, Object.getOwnPropertyDescriptor(definition, propertyName));
                    }

                    function glueProperties(obj, properties) {
                        var keys = Object.keys(properties);
                        for (var i = 0; i < keys.length; i++) {
                            var propertyName = keys[i];
                            var propertyGlue = properties[propertyName];
                            var propertySimpleName;
                            var glueOpenMethod = false;
                            if (propertyGlue.indexOf("open ") >= 0) {
                                propertySimpleName = propertyGlue.substring(5);
                                glueOpenMethod = true;
                            } else {
                                propertySimpleName = propertyGlue;
                            }
                            release || assert(Shumway.isString(propertySimpleName), "Make sure it's not a function.");
                            var qn = Multiname.getQualifiedName(Multiname.fromSimpleName(propertySimpleName));
                            if (glueOpenMethod) {
                                qn = Shumway.AVM2.Runtime.VM_OPEN_METHOD_PREFIX + qn;
                            }
                            release || assert(Shumway.isString(qn));
                            var descriptor = Object.getOwnPropertyDescriptor(obj, qn);
                            if (descriptor && descriptor.get) {
                                Object.defineProperty(obj, propertyName, descriptor);
                            } else {
                                Object.defineProperty(obj, propertyName, {
                                    get: new Function("", "return this." + qn),
                                    set: new Function("v", "this." + qn + " = v")
                                });
                            }
                        }
                    }

                    function generatePropertiesFromTraits(traits) {
                        var properties = createEmptyObject();
                        traits.forEach(function (trait) {
                            var ns = trait.name.getNamespace();
                            if (!ns.isPublic()) {
                                return;
                            }
                            properties[trait.name.getName()] = (trait.isMethod() ? "open " : "") + "public " + trait.name.getName();
                        });
                        return properties;
                    }

                    var glue = definition.__glue__;
                    if (!glue) {
                        return;
                    }

                    // Accessors for script properties from within AVM2.
                    if (glue.script) {
                        if (glue.script.instance) {
                            if (Shumway.isNumber(glue.script.instance)) {
                                release || assert(glue.script.instance === Glue.ALL);
                                glueProperties(dynamicPrototype, generatePropertiesFromTraits(this.classInfo.instanceInfo.traits));
                            } else {
                                glueProperties(dynamicPrototype, glue.script.instance);
                            }
                        }
                        if (glue.script.static) {
                            if (Shumway.isNumber(glue.script.static)) {
                                release || assert(glue.script.static === Glue.ALL);
                                glueProperties(this, generatePropertiesFromTraits(this.classInfo.traits));
                            } else {
                                glueProperties(this, glue.script.static);
                            }
                        }
                    }
                };

                Class.prototype.linkNatives = function (definition) {
                    var glue = definition.__glue__;

                    // assert (glue && glue.native);
                    // Binding to member methods marked as [native].
                    this.native = glue.native;
                };

                Class.prototype.verify = function () {
                    var instanceConstructor = this.instanceConstructor;
                    var tP = this.traitsPrototype;
                    var dP = this.dynamicPrototype;
                    release || assert(instanceConstructor && tP && dP);
                    release || assert(tP === instanceConstructor.prototype);
                    release || assert(dP === instanceConstructor.prototype || dP === Object.getPrototypeOf(instanceConstructor.prototype));
                    release || assert(Shumway.AVM2.Runtime.isClass(this));
                    if (tP !== Object.prototype) {
                        // TODO: Don't remember why I had this assertion.
                        // We don't want to put "class" on the Object.prototype.
                        // release || assert (Object.hasOwnProperty.call(tP, "class"));
                    }
                    release || assert(instanceConstructor.class === this);
                };

                Class.prototype.coerce = function (value) {
                    return value;
                };

                Class.prototype.isInstanceOf = function (value) {
                    // TODO: Fix me.
                    return this.isInstance(value);
                };

                Class.prototype.isInstance = function (value) {
                    if (value === null || typeof value !== "object") {
                        return false;
                    }
                    return this.dynamicPrototype.isPrototypeOf(value);
                };

                Class.prototype.trace = function (writer) {
                    var description = this.debugName + (this.baseClass ? " extends " + this.baseClass.debugName : "");
                    writer.enter("class " + description + " {");
                    writer.writeLn("scope: " + this.scope);
                    writer.writeLn("baseClass: " + this.baseClass);
                    writer.writeLn("classInfo: " + this.classInfo);
                    writer.writeLn("dynamicPrototype: " + this.dynamicPrototype);
                    writer.writeLn("traitsPrototype: " + this.traitsPrototype);
                    writer.writeLn("dynamicPrototype === traitsPrototype: " + (this.dynamicPrototype === this.traitsPrototype));

                    writer.writeLn("instanceConstructor: " + this.instanceConstructor);
                    writer.writeLn("instanceConstructorNoInitialize: " + this.instanceConstructorNoInitialize);
                    writer.writeLn("instanceConstructor === instanceConstructorNoInitialize: " + (this.instanceConstructor === this.instanceConstructorNoInitialize));

                    var traitsPrototype = this.traitsPrototype;
                    writer.enter("traitsPrototype: ");
                    if (traitsPrototype) {
                        writer.enter("VM_SLOTS: ");
                        writer.writeArray(traitsPrototype.asSlots.byID.map(function (slot) {
                            return slot.trait;
                        }));
                        writer.outdent();

                        writer.enter("VM_BINDINGS: ");
                        writer.writeArray(traitsPrototype.asBindings.map(function (binding) {
                            var pd = Object.getOwnPropertyDescriptor(traitsPrototype, binding);
                            var str = binding;
                            if (pd.get || pd.set) {
                                if (pd.get) {
                                    str += " getter: " + debugName(pd.get);
                                }
                                if (pd.set) {
                                    str += " setter: " + debugName(pd.set);
                                }
                            } else {
                                str += " value: " + debugName(pd.value);
                            }
                            return str;
                        }));
                        writer.outdent();

                        writer.enter("VM_OPEN_METHODS: ");
                        writer.writeArray(toKeyValueArray(traitsPrototype.asOpenMethods).map(function (pair) {
                            return pair[0] + ": " + debugName(pair[1]);
                        }));
                        writer.outdent();
                    }

                    writer.enter("classBindings: ");
                    this.classBindings.trace(writer);
                    writer.outdent();

                    writer.enter("instanceBindings: ");
                    this.instanceBindings.trace(writer);
                    writer.outdent();

                    writer.outdent();
                    writer.writeLn("call: " + this.call);
                    writer.writeLn("apply: " + this.apply);

                    writer.leave("}");
                };

                Class.prototype.toString = function () {
                    return "[class " + this.classInfo.instanceInfo.name.name + "]";
                };
                Class.OWN_INITIALIZE = 0x1;
                Class.SUPER_INITIALIZE = 0x2;
                return Class;
            })();
            Runtime.Class = Class;

            var callable = Shumway.AVM2.Runtime.ApplicationDomain.coerceCallable(Class);
            defineNonEnumerableProperty(Class, "call", callable.call);
            defineNonEnumerableProperty(Class, "apply", callable.apply);

            Class.instanceConstructor = Class;
            Class.toString = Class.prototype.toString;

            // Traits are below the dynamic instant prototypes,
            // i.e. this.dynamicPrototype === Object.getPrototypeOf(this.instanceConstructor.prototype)
            // and we cache the dynamic instant prototype as this.dynamicPrototype.
            //
            // Traits are not visible to the AVM script.
            Class.native = {
                instance: {
                    prototype: {
                        get: function () {
                            return this.dynamicPrototype;
                        }
                    }
                }
            };
        })(AVM2.Runtime || (AVM2.Runtime = {}));
        var Runtime = AVM2.Runtime;
    })(Shumway.AVM2 || (Shumway.AVM2 = {}));
    var AVM2 = Shumway.AVM2;
})(Shumway || (Shumway = {}));

var Interface = Shumway.AVM2.Runtime.Interface;
var Class = Shumway.AVM2.Runtime.Class;
